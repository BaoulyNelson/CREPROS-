from django.urls import path

from . import views

app_name = 'documents_app'

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='liste'),
    path('<slug:slug>/', views.DocumentDetailView.as_view(), name='detail'),
    path('<slug:slug>/telecharger/', views.telecharger_document, name='telecharger'),

    # ── Tableau de bord : Documents ────────────────────────────────────────
    path('tableau-de-bord/documents/',
         views.VueDashboardDocuments.as_view(), name='dashboard_documents'),
    path('tableau-de-bord/documents/nouveau/',
         views.VueDashboardCreerDocument.as_view(), name='dashboard_creer_document'),
    path('tableau-de-bord/documents/<int:pk>/modifier/',
         views.VueDashboardModifierDocument.as_view(), name='dashboard_modifier_document'),
    path('tableau-de-bord/documents/<int:pk>/supprimer/',
         views.VueDashboardSupprimerDocument.as_view(), name='dashboard_supprimer_document'),

    # ── Tableau de bord : Catégories de documents ──────────────────────────
    path('tableau-de-bord/categories/',
         views.VueDashboardCategoriesDocuments.as_view(), name='dashboard_categories_documents'),
    path('tableau-de-bord/categories/nouvelle/',
         views.VueDashboardCreerCategorieDocument.as_view(), name='dashboard_creer_categorie_document'),
    path('tableau-de-bord/categories/<int:pk>/modifier/',
         views.VueDashboardModifierCategorieDocument.as_view(), name='dashboard_modifier_categorie_document'),
    path('tableau-de-bord/categories/<int:pk>/supprimer/',
         views.VueDashboardSupprimerCategorieDocument.as_view(), name='dashboard_supprimer_categorie_document'),
]
