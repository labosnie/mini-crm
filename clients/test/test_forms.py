from django.test import TestCase
from clients.forms import ClientForm


class ClientFormTest(TestCase):
    def test_client_form_valid(self):
        """Test un formulaire valide"""
        form_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@example.com",
            "telephone": "0123456789",
            "adresse": "123 rue de Paris",
            "ville": "Paris",
            "code_postal": "75001",
            "pays": "France",
            "statut": "actif",
            "notes": "Client important"
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_form_invalid_email(self):
        """Test un formulaire avec email invalide"""
        form_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "email_invalide",  # Email invalide
            "telephone": "0123456789",
            "statut": "actif"
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_client_form_required_fields(self):
        """Test les champs obligatoires"""
        form_data = {
            "nom": "",  # Champ obligatoire vide
            "email": "",  # Champ obligatoire vide
            "statut": "actif"
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nom", form.errors)
        self.assertIn("email", form.errors)

    def test_client_form_optional_fields(self):
        """Test les champs optionnels"""
        form_data = {
            "nom": "Dupont",
            "email": "jean.dupont@example.com",
            "statut": "actif"
            # Les autres champs sont optionnels
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid()) 