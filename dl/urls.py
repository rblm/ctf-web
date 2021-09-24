from django.urls import path

from . import views

app_name="dl"

urlpatterns = [
    path('dl/<str:filename>', views.download, name='download'),
    path(r'dl/', views.download, name='download'),
    path(r'thanks/', views.thanks, name='thanks'),
    path('', views.download, name='download'),
]
