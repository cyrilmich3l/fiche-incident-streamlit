import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
from datetime import time
# ---------------------------------------------------------
# 1) FONCTION D’ENVOI DE MAIL VIA MAILJET
# ---------------------------------------------------------
def envoyer_mail(date_incident, type_evt, gravite, lieu, personnes_impliquees_str, contenu, destinataire):
    smtp_server = "in-v3.mailjet.com"
    smtp_port = 587
    username = "VOTRE_API_KEY"   # API KEY
    password = "VOTRE_SECRET_KEY"   # SECRET KEY

    # Objet dynamique
    objet_mail = (
        f"Incident {date_incident.strftime('%Y-%m-%d')} | "
        f"{', '.join(type_evt)} | "
        f"Gravité {gravite} | "
        f"{lieu} | "
        f"{personnes_impliquees_str}"
    )

    msg = MIMEText(contenu)
    msg["Subject"] = objet_mail
    msg["From"] = "VOTRE_ADRESSE_MAIL"
    msg["To"] = destinataire

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)


# ---------------------------------------------------------
# 2) CHARGEMENT DES DONNÉES
# ---------------------------------------------------------
personnes_df = pd.read_excel("personnes.xlsx")
personnes_df["Affichage"] = personnes_df.apply(
    lambda row: f"{row['Nom']} {row['Prénom']} | {row['Rôle']} | {row['Service']}",
    axis=1
)

lieux_df = pd.read_excel("lieux.xlsx")

st.title("Fiche incident")

# ---------------------------------------------------------
# 3) INFORMATIONS RÉDACTEUR
# ---------------------------------------------------------
st.markdown("### Informations rédacteur")

redacteur_affichage = st.selectbox(
    "Personne rédigeant la fiche",
    options=personnes_df["Affichage"].tolist()
)

redacteur_info = personnes_df[personnes_df["Affichage"] == redacteur_affichage].iloc[0]
redacteur_nom = redacteur_info["Nom"]
redacteur_role = redacteur_info["Rôle"]
redacteur_service = redacteur_info["Service"]

# ---------------------------------------------------------
# 4) INFOS INCIDENT
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    date_incident = st.date_input("Date", value=datetime.today())
with col2:
    heure_incident = st.time_input("Heure", value=time(8, 0))
with col3:
    lieu = st.selectbox("Lieu", options=lieux_df["Lieu"].unique())

# ---------------------------------------------------------
# 5) PERSONNES IMPLIQUÉES
# ---------------------------------------------------------
st.markdown("### Personnes impliquées")

if "nb_implique" not in st.session_state:
    st.session_state.nb_implique = 1

col_add, col_remove = st.columns(2)

with col_add:
    if st.button("➕ Ajouter une personne impliquée"):
        st.session_state.nb_implique += 1

with col_remove:
    if st.button("➖ Retirer la dernière personne"):
        if st.session_state.nb_implique > 1:
            st.session_state.nb_implique -= 1

personnes_impliquees = []

for i in range(st.session_state.nb_implique):
    personne_affichage = st.selectbox(
        f"Personne impliquée n°{i+1}",
        options=["Aucune"] + personnes_df["Affichage"].tolist(),
        key=f"implique_{i}"
    )

    if personne_affichage != "Aucune":
        info = personnes_df[personnes_df["Affichage"] == personne_affichage].iloc[0]
        personnes_impliquees.append(
            f"{info['Nom']} ({info['Rôle']} - {info['Service']})"
        )

personnes_impliquees_str = " / ".join(personnes_impliquees) if personnes_impliquees else "Aucune"

# ---------------------------------------------------------
# 6) DESCRIPTION
# ---------------------------------------------------------
st.markdown("### Description de l'évènement")

col_type, col_gravite = st.columns(2)
with col_type:
    type_evt = st.multiselect("Type", options=["Sécurité", "Qualité", "Autre"])
with col_gravite:
    gravite = st.radio("Gravité", options=["Presque accident", "Incident", "Accident"])

description = st.text_area("Description de l'évènement")
dommages = st.text_area("Dommages liés à l'évènement")
mesures = st.text_area("Mesures prises")

photo = st.file_uploader("Ajouter une photo (optionnel)", type=["png", "jpg", "jpeg"])

# ---------------------------------------------------------
# 7) PERSONNE CONTACTÉE
# ---------------------------------------------------------
st.markdown("### Personne contactée")

personne_contactee_affichage = st.selectbox(
    "Personne contactée pour régler le problème",
    options=["Personne"] + personnes_df["Affichage"].tolist()
)

# Extraction propre des infos
if personne_contactee_affichage != "Personne":
    info_contact = personnes_df[personnes_df["Affichage"] == personne_contactee_affichage].iloc[0]
    personne_contactee = f"{info_contact['Nom']} {info_contact['Prénom']} ({info_contact['Rôle']} - {info_contact['Service']})"
else:
    personne_contactee = "Personne"


# ---------------------------------------------------------
# 8) ENREGISTREMENT EXCEL
# ---------------------------------------------------------
def enregistrer_incident(
    redacteur_nom, redacteur_role, redacteur_service,
    date_incident, heure_incident, lieu,
    personnes_impliquees_str, type_evt, gravite,
    description, dommages, mesures,
    personne_contactee, photo_path=None
):
    new_row = {
        "Timestamp envoi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Rédacteur": redacteur_nom,
        "Rôle rédacteur": redacteur_role,
        "Service rédacteur": redacteur_service,
        "Date événement": date_incident,
        "Heure événement": heure_incident,
        "Lieu": lieu,
        "Personnes impliquées": personnes_impliquees_str,
        "Type": ", ".join(type_evt),
        "Gravité": gravite,
        "Description": description,
        "Dommages": dommages,
        "Mesures prises": mesures,
        "Personne contactée": personne_contactee,
        "Photo": photo_path if photo_path else ""
    }

    if os.path.exists("incidents.xlsx"):
        df = pd.read_excel("incidents.xlsx")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_excel("incidents.xlsx", index=False)

# ---------------------------------------------------------
# 9) CONTENU DU MAIL
# ---------------------------------------------------------
contenu_mail = f"""
FICHE INCIDENT

Rédacteur : {redacteur_nom} ({redacteur_role} - {redacteur_service})
Date : {date_incident}
Heure : {heure_incident}
Lieu : {lieu}

Personnes impliquées :
{personnes_impliquees_str}

Type d'événement : {type_evt}
Gravité : {gravite}

Description :
{description}

Dommages :
{dommages}

Mesures prises :
{mesures}

Personne contactée :
{personne_contactee}
"""

# ---------------------------------------------------------
# 10) BOUTON FINAL — ENREGISTREMENT + MAILJET
# ---------------------------------------------------------
if st.button("Envoyer la fiche incident", key="btn_envoyer"):
    photo_path = None
    if photo is not None:
        os.makedirs("photos_incidents", exist_ok=True)
        photo_path = os.path.join("photos_incidents", photo.name)
        with open(photo_path, "wb") as f:
            f.write(photo.getbuffer())

    enregistrer_incident(
        redacteur_nom, redacteur_role, redacteur_service,
        date_incident, heure_incident, lieu,
        personnes_impliquees_str, type_evt, gravite,
        description, dommages, mesures,
        personne_contactee, photo_path
    )

    try:
        envoyer_mail(
            date_incident, type_evt, gravite, lieu,
            personnes_impliquees_str, contenu_mail,
            "ADRESSE_MAIL_DESTINATAIRE"
        )
        st.success("Fiche envoyée avec succès")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi du mail : {e}")
