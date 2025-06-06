# Generated by Django 5.2.1 on 2025-05-24 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Projet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titre", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField(blank=True, null=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("en_cours", "En cours"),
                            ("termine", "Terminé"),
                            ("en_attente", "En attente"),
                            ("annule", "Annulé"),
                        ],
                        default="en_attente",
                        max_length=20,
                    ),
                ),
                (
                    "montant",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_modification", models.DateTimeField(auto_now=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projets",
                        to="clients.client",
                    ),
                ),
            ],
            options={
                "verbose_name": "Projet",
                "verbose_name_plural": "Projets",
            },
        ),
    ]
