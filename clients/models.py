from django.db import models
from django.contrib.auth.models import User

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
    tags = models.ManyToManyField('Tag', blank=True, related_name='clients')
    
    
    
    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom else self.nom
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-date_creation']

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('appel', 'Appel téléphonique'),
        ('email', 'Email'),
        ('reunion', 'Réunion'),
        ('note', 'Note interne'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-date']

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    couleur = models.CharField(max_length=7, default="#000000")  # Format hexadécimal
    
    def __str__(self):
        return self.nom
