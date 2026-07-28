from django.urls import path

from . import views

app_name = 'documents_app'

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='liste'),
    path('<slug:slug>/', views.DocumentDetailView.as_view(), name='detail'),
    path('<slug:slug>/telecharger/', views.telecharger_document, name='telecharger'),
]
