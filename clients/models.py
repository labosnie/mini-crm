from django.db import models

# Create your models here.

class Client(models.Model):
    # Choix pour le statut
    STATUT_CHOICES = [
        ('prospect', 'Prospect'),
        ('actif', 'Client Actif'),
        ('inactif', 'Client Inactif'),
    ]

    # Champs existants
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    # Nouveaux champs
    prenom = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='prospect'
    )
    notes = models.TextField(blank=True, help_text="Notes et informations supplémentaires sur le client")
    
    
    
    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom else self.nom
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-date_creation']
