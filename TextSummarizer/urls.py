# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import redirect
# from django.views.generic import RedirectView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('Summarizer.URLs.api_urls')),  
#     path('ui/', include('Summarizer.URLs.ui_urls')),
#     # path('', lambda request: redirect('/ui/summarize/')), 
#     path('', RedirectView.as_view(url='/ui/')),
# ]


from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Summarizer.URLs.api_urls')),
    path('ui/',  include('Summarizer.URLs.ui_urls')),
    path('', RedirectView.as_view(url='/ui/')),
]

