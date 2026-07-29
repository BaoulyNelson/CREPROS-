"""Backends d'authentification personnalisés."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

Utilisateur = get_user_model()


class EmailOuUsernameBackend(ModelBackend):
    """
    Authentifie un utilisateur à partir de son nom d'utilisateur OU de son
    adresse email, indifféremment saisis dans le même champ du formulaire
    de connexion.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Utilisateur.USERNAME_FIELD)
        if username is None or password is None:
            return None

        try:
            utilisateur = Utilisateur.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except Utilisateur.DoesNotExist:
            # Même comportement que ModelBackend : on exécute quand même le
            # hachage du mot de passe pour éviter une attaque par timing
            # révélant l'existence ou non du compte.
            Utilisateur().set_password(password)
            return None
        except Utilisateur.MultipleObjectsReturned:
            return None

        if utilisateur.check_password(password) and self.user_can_authenticate(utilisateur):
            return utilisateur
        return None