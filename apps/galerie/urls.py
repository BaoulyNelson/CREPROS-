from django.urls import path

from . import views

app_name = 'galerie'

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='liste'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='detail'),
]
