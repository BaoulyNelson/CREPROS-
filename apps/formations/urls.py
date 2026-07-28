from django.urls import path

from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.FormationListView.as_view(), name='liste'),
    path('<slug:slug>/', views.FormationDetailView.as_view(), name='detail'),
    path('<slug:slug>/inscription/', views.InscriptionFormationView.as_view(), name='inscription'),
]
