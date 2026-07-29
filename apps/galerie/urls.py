from django.urls import path

from . import views

app_name = 'galerie'

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='liste'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='detail'),

    # ── Tableau de bord : Albums photo ─────────────────────────────────────
    path('tableau-de-bord/albums/',
         views.VueDashboardAlbums.as_view(), name='dashboard_albums'),
    path('tableau-de-bord/albums/nouveau/',
         views.VueDashboardCreerAlbum.as_view(), name='dashboard_creer_album'),
    path('tableau-de-bord/albums/<int:pk>/modifier/',
         views.VueDashboardModifierAlbum.as_view(), name='dashboard_modifier_album'),
    path('tableau-de-bord/albums/<int:pk>/supprimer/',
         views.VueDashboardSupprimerAlbum.as_view(), name='dashboard_supprimer_album'),
    path('tableau-de-bord/albums/<int:pk>/photos/',
         views.VueDashboardGererPhotos.as_view(), name='dashboard_gerer_photos'),
    path('tableau-de-bord/photos/<int:pk>/supprimer/',
         views.VueDashboardSupprimerPhoto.as_view(), name='dashboard_supprimer_photo'),

    # ── Tableau de bord : Vidéos ────────────────────────────────────────────
    path('tableau-de-bord/videos/',
         views.VueDashboardVideos.as_view(), name='dashboard_videos'),
    path('tableau-de-bord/videos/nouvelle/',
         views.VueDashboardCreerVideo.as_view(), name='dashboard_creer_video'),
    path('tableau-de-bord/videos/<int:pk>/modifier/',
         views.VueDashboardModifierVideo.as_view(), name='dashboard_modifier_video'),
    path('tableau-de-bord/videos/<int:pk>/supprimer/',
         views.VueDashboardSupprimerVideo.as_view(), name='dashboard_supprimer_video'),
]
