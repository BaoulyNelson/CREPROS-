from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'comptes'

urlpatterns = [
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.DeconnexionView.as_view(), name='deconnexion'),
    path('tableau-de-bord/', views.TableauDeBordView.as_view(), name='tableau_de_bord'),
    path('profil/', views.ProfilView.as_view(), name='profil'),

    # --- Réinitialisation du mot de passe ---
    path(
        'mot-de-passe-oublie/',
        auth_views.PasswordResetView.as_view(
            template_name='comptes/mot_de_passe_oublie.html',
            email_template_name='comptes/email_reinitialisation.html',
            success_url=reverse_lazy('comptes:mot_de_passe_oublie_envoye'),
        ),
        name='mot_de_passe_oublie',
    ),
    path(
        'mot-de-passe-oublie/envoye/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='comptes/mot_de_passe_oublie_envoye.html',
        ),
        name='mot_de_passe_oublie_envoye',
    ),
    path(
        'reinitialiser/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='comptes/reinitialiser_mot_de_passe.html',
            success_url=reverse_lazy('comptes:reinitialisation_terminee'),
        ),
        name='reinitialiser_mot_de_passe',
    ),
    path(
        'reinitialisation-terminee/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='comptes/reinitialisation_terminee.html',
        ),
        name='reinitialisation_terminee',
    ),
    
path(
    'changer-mot-de-passe/',
    auth_views.PasswordChangeView.as_view(
        template_name='comptes/changer_mot_de_passe.html',
        success_url=reverse_lazy('comptes:changer_mot_de_passe_termine'),
    ),
    name='changer_mot_de_passe',
),
path(
    'changer-mot-de-passe/termine/',
    auth_views.PasswordChangeDoneView.as_view(
        template_name='comptes/changer_mot_de_passe_termine.html',
    ),
    name='changer_mot_de_passe_termine',
),
]
