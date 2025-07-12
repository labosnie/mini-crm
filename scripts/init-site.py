#!/usr/bin/env python
"""
Script d'initialisation du site Django pour la production
"""
import os
import django

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_crm.settings")
django.setup()

from django.contrib.sites.models import Site


def init_site():
    """Initialise le site Django avec les bonnes informations"""
    try:
        # Récupère ou crée le site par défaut
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={"domain": "mini-crm-lezi.onrender.com", "name": "Mini CRM Demo"},
        )

        # Met à jour les informations si nécessaire
        if not created:
            site.domain = "mini-crm-lezi.onrender.com"
            site.name = "Mini CRM Demo"
            site.save()

        print(f"✅ Site configuré: {site.name} ({site.domain})")

    except Exception as e:
        print(f"❌ Erreur lors de la configuration du site: {e}")


if __name__ == "__main__":
    init_site()
