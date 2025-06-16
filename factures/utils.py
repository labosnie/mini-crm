from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.conf import settings
import os
from societe.models import Societe


def generate_facture_pdf(facture):
    # Crée le dossier si besoin
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)

    # Chemin du fichier PDF
    filename = f"facture_{facture.id}.pdf"
    file_path = os.path.join(pdf_dir, filename)

    # Crée le document PDF
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
    )

    # Contenu
    elements = []

    # En-tête entreprise/client
    societe = Societe.objects.first()
    if not societe:
        # Valeurs par défaut si jamais
        societe = type(
            "Societe",
            (),
            {
                "nom": "Votre Société",
                "adresse": "Adresse",
                "code_postal": "CP",
                "ville": "Ville",
                "telephone": "Téléphone",
                "email": "Email",
                "siret": "",
                "tva": "",
                "iban": "",
                "bic": "",
            },
        )()
    header_data = [
        [
            Paragraph(
                f"<b>{societe.nom}</b><br/>{societe.adresse}<br/>{societe.code_postal} {societe.ville}<br/>"
                f"Tél : {societe.telephone}<br/>{societe.email}",
                styles["Normal"],
            ),
            Paragraph(
                f"<b>{facture.client.nom}</b><br/>{facture.client.adresse}<br/>{facture.client.email}",
                styles["Normal"],
            ),
        ]
    ]
    header_table = Table(header_data, colWidths=[8 * cm, 8 * cm])
    header_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # Titre
    elements.append(
        Paragraph('<para align="center"><b>FACTURE</b></para>', styles["Title"])
    )
    elements.append(Spacer(1, 12))

    # Infos facture
    infos = f"""
    <b>Numéro de facture :</b> {facture.numero}<br/>
    <b>Date de facture :</b> {facture.date_emission.strftime('%d/%m/%Y')}<br/>
    <b>N° client :</b> {facture.client.id}
    """
    elements.append(Paragraph(infos, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Tableau des lignes de facture
    data = [["Description", "Quantité", "Unité", "Prix unitaire HT", "Total HT", "TVA"]]
    # Remplace ceci par tes vraies lignes si tu as un modèle LigneFacture relié à Facture
    for ligne in getattr(
        facture, "lignes", []
    ):  # ou facture.lignefacture_set.all() si related_name absent
        data.append(
            [
                ligne.description,
                str(ligne.quantite),
                ligne.unite,
                f"{ligne.prix_unitaire:.2f} €",
                f"{ligne.total_ht:.2f} €",
                f"{ligne.tva} 20%",
            ]
        )
    # Si tu n'as pas de lignes, ajoute une ligne factice :
    if len(data) == 1:
        data.append(
            [
                "Projet : " + facture.projet.titre,
                "1",
                "",
                f"{facture.montant:.2f} €",
                f"{facture.montant:.2f} €",
                "20 %",
            ]
        )

    table = Table(data, colWidths=[5 * cm, 2 * cm, 2 * cm, 3 * cm, 3 * cm, 2 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Totaux
    TAUX_TVA = 0.20  # 20%
    montant_ht = float(facture.montant) / (1 + TAUX_TVA)
    tva = float(facture.montant) - montant_ht
    totaux_data = [
        ["Total HT", f"{montant_ht:.2f} €"],
        [f"TVA ({int(TAUX_TVA*100)}%)", f"{tva:.2f} €"],
        ["Total TTC", f"{facture.montant:.2f} €"],
    ]
    totaux_table = Table(totaux_data, colWidths=[4 * cm, 4 * cm], hAlign="RIGHT")
    totaux_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )
    elements.append(totaux_table)
    elements.append(Spacer(1, 12))

    # Conditions de paiement
    elements.append(
        Paragraph(
            "Conditions de paiement : 30% à la commande, paiement à réception de facture<br/>"
            "Mode de paiement : virement ou chèque",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 8))
    elements.append(
        Paragraph(
            "Nous vous remercions de votre confiance.<br/>Cordialement.",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 16))
    pied = (
        f"<b>{societe.nom}</b> - {societe.adresse} - {societe.telephone} - {societe.email}<br/>"
        f"IBAN : {societe.iban} - BIC : {societe.bic}<br/>"
        f"SIRET : {societe.siret} - TVA : {societe.tva}"
    )
    elements.append(Paragraph(pied, styles["Normal"]))

    # Génère le PDF
    doc.build(elements)

    return file_path
