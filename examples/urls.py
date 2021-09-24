from django.urls import path

from . import views

app_name="examples"

urlpatterns = [
    path('download/<str:filename>', views.download, name='download'),
    #path('download/<str:filename>/<str:pw>/<str:pin>', views.download, name='download'),
    path('download', views.download, name='download'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('creds/<str:filename>', views.CredsView.as_view(), name='creds'),
    #path(r'creds/(?P<filename>\w+)/$', views.CredsView.as_view(), name='creds'),
    #path('creds', views.download, name='download'),
    path('', views.download, name='download'),
]
