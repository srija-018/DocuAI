from django.shortcuts import render
from django.http import JsonResponse
from db.db_handler import fetch_recipients


# -------------------------------------- HOME PAGE VIEW --------------------------------------
def home_view(request):
    return render(request, "Summarizer/index.html")


# -------------------------------------- SUMMARIZE / CHATBOT UI VIEW --------------------------------------
def summarize_ui_view(request):
    view_mode = request.GET.get("view", "summarize")  
    return render(request, "Summarizer/summarize.html", {"view_mode": view_mode})


# -------------------------------------- GET RECIPIENT EMAILS --------------------------------------
def get_recipient_emails(request):
    try:
        data = fetch_recipients()
        return JsonResponse({"recipients": data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
