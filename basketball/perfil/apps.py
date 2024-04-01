from django.apps import AppConfig
from allauth.account.signals import user_signed_up


class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfil'

