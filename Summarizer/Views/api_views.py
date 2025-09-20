import os
import re
import json
import mimetypes
import fitz  
from datetime import datetime
from docx import Document
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Summarizer.models import ContentModel
from AIModels.Gemini.gemini import GeminiChat
from AIModels.Handlers.ai_handler import AIHandler
from Content.FileSummary.file_handler import FileContentHandler



# ---------------------------------------------------- HELPER FUNCTION ----------------------------------------------------
@csrf_exempt
def save_summary_to_file(summary: str, original_name: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(original_name)[0]
    summary_filename = f"{base_name}_summary_{timestamp}.txt"
    summary_dir = os.path.join(settings.MEDIA_ROOT, "summaries")
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, summary_filename)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    summary_url = os.path.join(settings.MEDIA_URL, "summaries", summary_filename)
    return summary_filename, summary_url



# ---------------------------------------------------- MULTIPLE FILE SUMMARIZATION ----------------------------------------------------
@csrf_exempt
def summarize_multiple_files(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    files = request.FILES.getlist('files')
    if not files:
        return JsonResponse({'error': 'No files uploaded'}, status=400)

    try:
        combined_text = ""

        for f in files:
            filename = f.name.lower()
            if filename.endswith('.txt'):
                text = f.read().decode('utf-8', errors='ignore')
            elif filename.endswith('.docx'):
                doc = Document(f)
                text = '\n'.join([para.text for para in doc.paragraphs])
            elif filename.endswith('.pdf'):
                text = ""
                pdf = fitz.open(stream=f.read(), filetype="pdf")
                for page in pdf:
                    text += page.get_text()
            else:
                return JsonResponse({'error': f"Unsupported file type: {filename}"}, status=400)
            combined_text += f"\n\n--- {filename} ---\n\n" + text

        combined_text = combined_text[:15000]
        gemini = GeminiChat()
        summary = gemini.summarize(f"Summarize the following content:\n\n{combined_text}")

        summary_filename, summary_url = save_summary_to_file(summary, "combined_summary")
        return JsonResponse({
            'summary': summary,
            'summary_filename': summary_filename,
            'summary_file_url': summary_url
        })

    except Exception as e:
        return JsonResponse({'error': f"Error during processing: {str(e)}"}, status=500)



# ---------------------------------------------------- SINGLE FILE SUMMARIZATION ----------------------------------------------------
def summarize_file_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({"error": "File not provided"}, status=400)

    try:
        content = FileContentHandler.extract_text(uploaded_file)
        model = AIHandler().get_model("file")
        summary = model.summarize(content)
        summary_filename, summary_url = save_summary_to_file(summary, uploaded_file.name)
        return JsonResponse({
            "summary": summary,
            "summary_file_url": summary_url,
            "summary_filename": summary_filename
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# ---------------------------------------------------- UPLOAD FILES TO DATABASE ----------------------------------------------------
@csrf_exempt
def upload_file_to_db(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    uploaded_files = request.FILES.getlist('db_files')
    if not uploaded_files:
        return JsonResponse({'error': 'No files uploaded.'}, status=400)

    inserted = []
    skipped = []

    for file in uploaded_files:
        filename = file.name
        mimetype, _ = mimetypes.guess_type(filename)
        if not mimetype:
            return JsonResponse({'error': f"Unknown file type for {filename}."}, status=400)

        if ContentModel.objects.filter(title=filename).exists():
            skipped.append(filename)
            continue

        from Content.FileSummary.file_handler import FileContentHandler

        try:
            content = FileContentHandler.extract_text(file)
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"Failed to read {filename}: {str(e)}"}, status=500)

        try:
            ContentModel.objects.create(title=filename, content=content)
            inserted.append(filename)
        except Exception as e:
            return JsonResponse({'error': f"DB error for {filename}: {str(e)}"}, status=500)

    return JsonResponse({'success': True, 'inserted': inserted, 'skipped': skipped})



# ---------------------------------------------------- LIST FILE TITLES ----------------------------------------------------
def list_file_titles(request):
    titles = ContentModel.objects.values_list('title', flat=True)
    return JsonResponse({'titles': list(titles)})




# ---------------------------------------------------- SEND SUMMARY VIA EMAIL ----------------------------------------------------
@csrf_exempt
def send_summary_email(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    file_path = None
    try:
        to_email = request.POST.get("email", "").strip()
        file_title = request.POST.get("file_title", "").strip()
        if not to_email or not file_title:
            return JsonResponse({"error": "Email and file title are required"}, status=400)

        summary_dir = os.path.join(settings.MEDIA_ROOT, "summaries")
        matching_files = [f for f in os.listdir(summary_dir) if file_title in f]
        if not matching_files:
            return JsonResponse({"error": "Summary file not found."}, status=404)

        latest_file = sorted(matching_files)[-1]
        file_path = os.path.join(summary_dir, latest_file)

        email = EmailMessage(
            subject=f"Summary for {file_title}",
            body="Please find the summary attached.",
            to=[to_email]
        )
        email.attach_file(file_path)
        email.send()

        return JsonResponse({"success": True, "message": f"Email sent to {to_email}."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted summary file: {file_path}")
            except Exception as cleanup_error:
                print(f"Failed to delete file {file_path}: {cleanup_error}")



# ---------------------------------------------------- SEMANTIC SEARCH / Q&A ----------------------------------------------------
@csrf_exempt
def semantic_search_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        question = body.get("question", "").strip()
        if not question:
            return JsonResponse({"error": "Question is required."}, status=400)

        content_qs = ContentModel.objects.all()
        documents = [obj.content for obj in content_qs]
        titles = [obj.title for obj in content_qs]

        if not documents:
            return JsonResponse({"error": "No documents found in database."}, status=404)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents + [question])
        question_vec = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]

        similarities = cosine_similarity(question_vec, doc_vectors).flatten()
        top_indices = similarities.argsort()[-3:][::-1]
        top_docs = [(titles[i], documents[i]) for i in top_indices]

        combined_content = ""
        for title, content in top_docs:
            combined_content += f"\n--- Title: {title} ---\n{content[:2000]}\n"

        model = AIHandler().get_model("semantic")
        prompt = f"""You are a smart assistant. Based on the content below, answer the following question.
Content:
{combined_content}
Question: {question}
"""
        answer = model.ask(prompt)

        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
