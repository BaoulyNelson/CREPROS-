from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.AccueilView.as_view(), name='accueil'),
    path('a-propos/', views.AProposView.as_view(), name='a_propos'),
    path('politique-de-confidentialite/', views.PolitiqueConfidentialiteView.as_view(), name='politique_confidentialite'),

    # ── Tableau de bord : Partenaires ───────────────────────────────────────
    path('tableau-de-bord/partenaires/',
         views.VueDashboardPartenaires.as_view(), name='dashboard_partenaires'),
    path('tableau-de-bord/partenaires/nouveau/',
         views.VueDashboardCreerPartenaire.as_view(), name='dashboard_creer_partenaire'),
    path('tableau-de-bord/partenaires/<int:pk>/modifier/',
         views.VueDashboardModifierPartenaire.as_view(), name='dashboard_modifier_partenaire'),
    path('tableau-de-bord/partenaires/<int:pk>/supprimer/',
         views.VueDashboardSupprimerPartenaire.as_view(), name='dashboard_supprimer_partenaire'),
]
