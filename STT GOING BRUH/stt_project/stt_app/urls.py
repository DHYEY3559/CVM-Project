from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('record/', views.record_audio, name='record'),
    path('upload/', views.upload_audio, name='upload'),
    path('results/', views.results, name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)