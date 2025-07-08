from datetime import timedelta
from django.utils.timezone import now
from .models import Evenement


class DeleteExpiredEventsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Calculer l'heure 1 heure après la date_heure de l'événement
        time_threshold = now()

        # Supprimer les événements dont la date_heure est inférieure à l'heure actuelle moins 1 heure
        Evenement.objects.filter(date_heure__lte=time_threshold - timedelta(hours=1)).delete()

        # Continuer avec la requête
        response = self.get_response(request)
        return response