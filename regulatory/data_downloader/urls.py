from django.urls import path
from . import views

app_name = 'data_downloader'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('update/', views.UpdateDBView, name='update'),
]
