import uuid
import qrcode
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from authentification.models import CustomUser

TYPE_EVENEMENT_CHOICES = [
    ('concert', 'Concert'),
    ('theatre', 'Théâtre'),
    ('sport', 'Sport'),
    ('conference', 'Conférence'),
    ('festival', 'Festival'),
    ('autre', 'Autre'),
]


class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to='evenements/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type_evenement = models.CharField(max_length=20, choices=TYPE_EVENEMENT_CHOICES)
    date_heure = models.DateTimeField()
    lieu = models.CharField(max_length=255)
    organisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:  # Si l'objet est en cours de création ou si le slug est vide
            base_slug = slugify(self.nom)
            unique_slug = base_slug
            num = 1

            # Vérifie l'unicité du slug
            while Evenement.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1

            self.slug = unique_slug
        elif self.pk:  # Si l'objet existe déjà (modification)
            original = Evenement.objects.get(pk=self.pk)
            if original.nom != self.nom:  # Si le nom a été modifié, mettre à jour le slug
                base_slug = slugify(self.nom)
                unique_slug = base_slug
                num = 1

                # Vérifie l'unicité du slug
                while Evenement.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{num}"
                    num += 1

                self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class CategorieEvenement(models.Model):
    nom = models.CharField(max_length=100)  # standard 5000fcfa, vip, vvip etc
    billets_restant = models.IntegerField(default=0)  # Nombre de places de l'evenement
    prix = models.IntegerField(default=0)
    evenement = models.ForeignKey(Evenement, related_name="categories", on_delete=models.CASCADE)


class QRCode(models.Model):
    categorie_evenement = models.ForeignKey('CategorieEvenement', on_delete=models.CASCADE)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True)
    valide = models.BooleanField(default=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"QR Code pour {self.categorie_evenement.evenement.nom}"

    # Méthode pour invalider le QR Code
    def invalider_qr_code(self):
        """Désactive ce QR Code en le rendant invalide."""
        self.valide = False
        self.save()

    # Méthode pour vérifier si le QR Code est valide
    def est_valide(self):
        """Vérifie si le QR Code est encore valide."""
        return self.valide

    def save(self, *args, **kwargs):
        if not self.qr_image:  # Générer le QRCode seulement si l'image n'existe pas
            qr_data = f"{self.token}"  # Stocker les informations du token
            qr = qrcode.make(qr_data)

            # Sauvegarde dans un fichier temporaire
            temp_path = f"qrcode_{self.token}.png"
            qr.save(temp_path)

            # Enregistrement dans l'image
            with open(temp_path, "rb") as f:
                self.qr_image.save(f"qrcode_{self.token}.png", File(f))

        super().save(*args, **kwargs)


class Historique(models.Model):
    acheteur = models.EmailField()
    evenement = models.CharField(max_length=100)
    categorie_evenement = models.CharField(max_length=100)
    prix_billet = models.IntegerField()
    nombre_places_payees = models.IntegerField()
    date_achat = models.DateTimeField(auto_now_add=True)


# Pour supprimer l'image lorsqu'on la supprime en bdd
@receiver(pre_delete, sender=Evenement)
def supprimer_image(sender, instance, **kwargs):
    if instance.photo:
        default_storage.delete(instance.photo.path)


# Pour supprimer la photo, lorsqu'on la modifie en bdd
@receiver(pre_save, sender=Evenement)
def supprimer_ancienne_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_obj = Evenement.objects.get(pk=instance.pk)
    except Evenement.DoesNotExist:
        return False

    new_image = instance.photo
    if old_obj.photo and old_obj.photo != new_image:
        # Supprimer l'ancien fichier du stockage
        default_storage.delete(old_obj.photo.path)


# Pour supprimer les QRCode images en bdd
@receiver(pre_delete, sender=QRCode)
def supprimer_qrcode(sender, instance, **kwargs):
    if instance.qr_image:
        default_storage.delete(instance.qr_image.path)


# Pour supprimer les qrcodes lorsqu'on la modifie en bdd
@receiver(pre_save, sender=QRCode)
def supprimer_ancien_qrcode(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_obj = QRCode.objects.get(pk=instance.pk)
    except QRCode.DoesNotExist:
        return False

    new_image = instance.qr_image
    if old_obj.qr_image and old_obj.qr_image != new_image:
        # Supprimer l'ancien fichier du stockage
        default_storage.delete(old_obj.qr_image.path)
