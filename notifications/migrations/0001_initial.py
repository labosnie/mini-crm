# Generated by Django 5.2.1 on 2025-06-15 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("factures", "0002_facture_date_echeance_alter_facture_statut_paiement"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ECHEANCE", "Échéance de paiement"),
                            ("RETARD", "Retard de paiement"),
                            ("CREATION", "Nouvelle facture"),
                            ("MODIFICATION", "Modification de facture"),
                        ],
                        max_length=20,
                    ),
                ),
                ("message", models.TextField()),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("lu", models.BooleanField(default=False)),
                ("date_lecture", models.DateTimeField(blank=True, null=True)),
                (
                    "facture",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="factures.facture",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_creation"],
            },
        ),
    ]
