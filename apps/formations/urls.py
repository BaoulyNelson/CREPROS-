from django.urls import path

from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.FormationListView.as_view(), name='liste'),
    path('<slug:slug>/', views.FormationDetailView.as_view(), name='detail'),
    path('<slug:slug>/inscription/', views.InscriptionFormationView.as_view(), name='inscription'),

    # ── Tableau de bord : Formations ───────────────────────────────────────
    path('tableau-de-bord/formations/',
         views.VueDashboardFormations.as_view(), name='dashboard_formations'),
    path('tableau-de-bord/formations/nouvelle/',
         views.VueDashboardCreerFormation.as_view(), name='dashboard_creer_formation'),
    path('tableau-de-bord/formations/<int:pk>/modifier/',
         views.VueDashboardModifierFormation.as_view(), name='dashboard_modifier_formation'),
    path('tableau-de-bord/formations/<int:pk>/supprimer/',
         views.VueDashboardSupprimerFormation.as_view(), name='dashboard_supprimer_formation'),

    # ── Tableau de bord : Inscriptions aux formations ──────────────────────
    path('tableau-de-bord/inscriptions/',
         views.VueDashboardInscriptions.as_view(), name='dashboard_inscriptions'),
    path('tableau-de-bord/inscriptions/<int:pk>/supprimer/',
         views.VueDashboardSupprimerInscription.as_view(), name='dashboard_supprimer_inscription'),
]
