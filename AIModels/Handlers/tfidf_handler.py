from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Summarizer.models import ContentModel

class TFIDFHandler:
    # Handles TF-IDF vectorization and similarity search over database content.

    def __init__(self):
        # Initialize the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.documents = list(ContentModel.objects.values_list("content", flat=True))
        self.titles = list(ContentModel.objects.values_list("title", flat=True))
        self.document_matrix = self.vectorizer.fit_transform(self.documents)

    def query(self, question: str, top_n: int = 1):
        # Takes a question string and returns the top_n most similar documents
        # based on cosine similarity of TF-IDF vectors.
        question_vector = self.vectorizer.transform([question])
        similarity_scores = cosine_similarity(question_vector, self.document_matrix).flatten()
        top_indices = similarity_scores.argsort()[::-1][:top_n]
        results = [(self.titles[i], self.documents[i], similarity_scores[i]) for i in top_indices if similarity_scores[i] > 0]
        return results
