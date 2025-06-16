from django.db import models


class Societe(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=30)
    email = models.EmailField()
    siret = models.CharField(max_length=20, blank=True)
    tva = models.CharField(max_length=30, blank=True)
    iban = models.CharField(max_length=40, blank=True)
    bic = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nom
