from django.urls import path
from Summarizer.Views.api_views import (
    summarize_file_api,
    upload_file_to_db,
    list_file_titles,
    send_summary_email,
    semantic_search_api,
    summarize_multiple_files,
)

urlpatterns = [
    path('summarize-file/', summarize_file_api, name='api-summarize'),
    path('upload-file-to-db/', upload_file_to_db, name='upload-file-to-db'),
    path('list-file-titles/', list_file_titles, name='list_file_titles'),
    path('send-summary-email/', send_summary_email, name='send_summary_email'),
    path('semantic-search/', semantic_search_api, name='semantic_search_api'),
    path('summarize-multiple-files/', summarize_multiple_files, name='summarize-multiple-files'),
]
