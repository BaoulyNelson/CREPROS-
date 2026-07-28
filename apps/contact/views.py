"""Vue publique du formulaire de contact."""
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MessageContactForm
from .models import MessageContact


class ContactView(CreateView):
    """Affiche et traite le formulaire de contact public."""

    model = MessageContact
    form_class = MessageContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:contact')

    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, "Votre message a bien été envoyé. Nous vous répondrons dans les plus brefs délais.")
        try:
            send_mail(
                subject=f"[Contact du site] {self.object.sujet}",
                message=(
                    f"Nom : {self.object.nom_complet}\n"
                    f"Email : {self.object.email}\n"
                    f"Téléphone : {self.object.telephone}\n\n"
                    f"{self.object.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL_DESTINATAIRE],
                fail_silently=True,
            )
        except Exception:
            # L'échec de l'envoi d'email ne doit jamais empêcher l'enregistrement du message.
            pass
        return reponse
