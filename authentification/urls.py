from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, DeleteUserAPIView

urlpatterns = [
    path('inscription/', RegisterAPIView.as_view(), name='inscription'),
    path('connexion/', LoginAPIView.as_view(), name='connexion'),
    path('deconnexion/', LogoutAPIView.as_view(), name='deconnexion'),
    path('suppression/', DeleteUserAPIView.as_view(), name='suppression'),
]
