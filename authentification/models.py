from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profil', blank=True, null=True)
    organisateur = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Pour supprimer l'image lorsqu'on la supprime en bdd
@receiver(pre_delete, sender=CustomUser)
def supprimer_photo(sender, instance, **kwargs):
    if instance.photo:
        default_storage.delete(instance.photo.path)


# Pour supprimer la photo, lorsqu'on la modifie en bdd
@receiver(pre_save, sender=CustomUser)
def supprimer_ancienne_photo(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_obj = CustomUser.objects.get(pk=instance.pk)
    except CustomUser.DoesNotExist:
        return False

    new_image = instance.photo
    if old_obj.photo and old_obj.photo != new_image:
        # Supprimer l'ancien fichier du stockage
        default_storage.delete(old_obj.photo.path)
