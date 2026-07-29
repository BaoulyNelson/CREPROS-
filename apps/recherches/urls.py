from django.urls import path

from . import views

app_name = 'recherches'

urlpatterns = [
    path('', views.RechercheListView.as_view(), name='liste'),
    path('<slug:slug>/', views.RechercheDetailView.as_view(), name='detail'),
    path('<slug:slug>/telecharger/', views.telecharger_recherche, name='telecharger'),

    # ── Tableau de bord : Recherches ───────────────────────────────────────
    path('tableau-de-bord/recherches/',
         views.VueDashboardRecherches.as_view(), name='dashboard_recherches'),
    path('tableau-de-bord/recherches/nouvelle/',
         views.VueDashboardCreerRecherche.as_view(), name='dashboard_creer_recherche'),
    path('tableau-de-bord/recherches/<int:pk>/modifier/',
         views.VueDashboardModifierRecherche.as_view(), name='dashboard_modifier_recherche'),
    path('tableau-de-bord/recherches/<int:pk>/supprimer/',
         views.VueDashboardSupprimerRecherche.as_view(), name='dashboard_supprimer_recherche'),

    # ── Tableau de bord : Catégories de recherche ──────────────────────────
    path('tableau-de-bord/categories/',
         views.VueDashboardCategoriesRecherche.as_view(), name='dashboard_categories_recherche'),
    path('tableau-de-bord/categories/nouvelle/',
         views.VueDashboardCreerCategorieRecherche.as_view(), name='dashboard_creer_categorie_recherche'),
    path('tableau-de-bord/categories/<int:pk>/modifier/',
         views.VueDashboardModifierCategorieRecherche.as_view(), name='dashboard_modifier_categorie_recherche'),
    path('tableau-de-bord/categories/<int:pk>/supprimer/',
         views.VueDashboardSupprimerCategorieRecherche.as_view(), name='dashboard_supprimer_categorie_recherche'),
]
