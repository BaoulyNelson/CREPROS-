"""Vues publiques de la galerie photos et vidéos, et tableau de bord."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import EditeurRequisMixin

from .forms import FormulaireAlbum, FormulairePhoto, FormulaireVideo
from .models import Album, Photo, Video


class AlbumListView(ListView):
    """Liste des albums photo (galerie principale)."""
    model = Album
    template_name = 'galerie/liste.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        return Album.objects.prefetch_related('photos')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['videos'] = Video.objects.all()[:6]
        return contexte


class AlbumDetailView(DetailView):
    """Détail d'un album avec toutes ses photos."""
    model = Album
    template_name = 'galerie/detail.html'
    context_object_name = 'album'


# ── Tableau de bord : Albums photo ────────────────────────────────────────────


class VueDashboardAlbums(EditeurRequisMixin, ListView):
    template_name = "dashboard/albums/liste.html"
    context_object_name = "albums"

    def get_queryset(self):
        return Album.objects.prefetch_related("photos")


class VueDashboardCreerAlbum(EditeurRequisMixin, CreateView):
    template_name = "dashboard/albums/formulaire.html"
    form_class = FormulaireAlbum

    def form_valid(self, form):
        messages.success(self.request, "Album créé avec succès ! Ajoutez maintenant des photos.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouvel album photo"
        ctx["bouton_submit"] = "Créer l'album"
        return ctx

    def get_success_url(self):
        return reverse("galerie:dashboard_gerer_photos", kwargs={"pk": self.object.pk})


class VueDashboardModifierAlbum(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/albums/formulaire.html"
    form_class = FormulaireAlbum
    queryset = Album.objects.all()
    success_url = reverse_lazy("galerie:dashboard_albums")

    def form_valid(self, form):
        messages.success(self.request, "Album mis à jour avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.titre}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerAlbum(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/albums/confirmer_suppression.html"
    queryset = Album.objects.all()
    success_url = reverse_lazy("galerie:dashboard_albums")

    def form_valid(self, form):
        messages.success(self.request, "Album supprimé avec succès.")
        return super().form_valid(form)


class VueDashboardGererPhotos(EditeurRequisMixin, DetailView):
    """Affiche les photos d'un album et un formulaire pour en ajouter de nouvelles."""

    template_name = "dashboard/albums/photos.html"
    model = Album
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["photos"] = self.object.photos.all()
        ctx["form"] = FormulairePhoto()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormulairePhoto(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = self.object
            photo.save()
            messages.success(request, "Photo ajoutée avec succès !")
            return redirect("galerie:dashboard_gerer_photos", pk=self.object.pk)
        messages.error(request, "Erreur lors de l'ajout de la photo.")
        ctx = self.get_context_data()
        ctx["form"] = form
        return self.render_to_response(ctx)


class VueDashboardSupprimerPhoto(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/albums/confirmer_suppression_photo.html"
    queryset = Photo.objects.all()

    def get_success_url(self):
        return reverse("galerie:dashboard_gerer_photos", kwargs={"pk": self.object.album_id})

    def form_valid(self, form):
        messages.success(self.request, "Photo supprimée avec succès.")
        return super().form_valid(form)


# ── Tableau de bord : Vidéos ───────────────────────────────────────────────────


class VueDashboardVideos(EditeurRequisMixin, ListView):
    template_name = "dashboard/videos/liste.html"
    context_object_name = "videos"
    queryset = Video.objects.all()


class VueDashboardCreerVideo(EditeurRequisMixin, CreateView):
    template_name = "dashboard/videos/formulaire.html"
    form_class = FormulaireVideo
    success_url = reverse_lazy("galerie:dashboard_videos")

    def form_valid(self, form):
        messages.success(self.request, "Vidéo ajoutée avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Ajouter une vidéo"
        ctx["bouton_submit"] = "Ajouter la vidéo"
        return ctx


class VueDashboardModifierVideo(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/videos/formulaire.html"
    form_class = FormulaireVideo
    queryset = Video.objects.all()
    success_url = reverse_lazy("galerie:dashboard_videos")

    def form_valid(self, form):
        messages.success(self.request, "Vidéo mise à jour avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.titre}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerVideo(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/videos/confirmer_suppression.html"
    queryset = Video.objects.all()
    success_url = reverse_lazy("galerie:dashboard_videos")

    def form_valid(self, form):
        messages.success(self.request, "Vidéo supprimée avec succès.")
        return super().form_valid(form)
