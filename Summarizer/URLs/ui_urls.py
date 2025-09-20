from django.urls import path
from Summarizer.Views.ui_views import (home_view,
                                     summarize_ui_view,
                                     get_recipient_emails)

urlpatterns = [
    path('', home_view, name='ui-home'),
    path('summarize/', summarize_ui_view, name='ui-summarize'),
    path('get-recipients/', get_recipient_emails, name='get_recipients'),
]