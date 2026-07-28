from django.urls import path

from . import views

app_name = 'recherches'

urlpatterns = [
    path('', views.RechercheListView.as_view(), name='liste'),
    path('<slug:slug>/', views.RechercheDetailView.as_view(), name='detail'),
    path('<slug:slug>/telecharger/', views.telecharger_recherche, name='telecharger'),
]
