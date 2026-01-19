# 📋 Application de Remontée d'Incidents

Cette application Streamlit permet de déclarer, enregistrer et transmettre des fiches d'incidents au sein d'une organisation.  
Elle facilite la traçabilité, la communication et le suivi des événements liés à la sécurité, la qualité ou tout autre type d'incident.

---

## 🚀 Fonctionnalités

### 🧑‍💼 Sélection du rédacteur
- Choix du rédacteur dans une liste dynamique issue d’un fichier Excel (`personnes.xlsx`)
- Affichage automatique du nom, rôle et service

### 📅 Informations sur l'incident
- Date et heure de l’événement
- Lieu sélectionné depuis un fichier de référence (`lieux.xlsx`)
- Ajout de plusieurs personnes impliquées avec affichage détaillé

### 📝 Description complète
- Type d’incident (Sécurité, Qualité, Autre)
- Gravité (Presque accident, Incident, Accident)
- Description libre
- Dommages
- Mesures prises
- Personne contactée (liste dynamique comme pour les personnes impliquées)

### 📸 Ajout de photo
- Upload d’une image
- Sauvegarde automatique dans un dossier dédié

### 📊 Enregistrement dans Excel
- Ajout automatique dans `incidents.xlsx`
- Ajout d’un timestamp d’envoi
- Conservation de toutes les informations structurées

### 📧 Envoi automatique par email (Mailjet)
- Objet dynamique incluant date, type, gravité, lieu et personnes impliquées
- Contenu détaillé de la fiche incident
- Envoi via SMTP Mailjet

---

## 📸 Aperçu de l’application

### 📨 Mail reçu
<img src="images/mail.png" width="600">

### 🖥️ Interface Streamlit
<img src="images/app_1.png" width="600">
<img src="images/app_2.png" width="600">

### 📊 Ligne Excel générée
<img src="images/excel.png" width="600">


## 🗂️ Structure du projet

📁 projet/
│── stream_incident.py
│── personnes.xlsx
│── lieux.xlsx
│── incidents.xlsx  (généré automatiquement)
│── 📁 photos_incidents/ (créé automatiquement)
│── README.md
│── 📁 image (screenshot de l'appli)



---
## 🔧 Installation

# Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/ton-projet.git
cd ton-projet

pip install -r requirements.txt ### 2️⃣ Installer les dépendances

streamlit run stream_incident.py ### 3️⃣ Lancer l’application
```

# 🔐 Configuration Mailjet
Dans stream_incident.py, configurez vos identifiants :

python
username = "VOTRE_API_KEY"
password = "VOTRE_SECRET_KEY"
msg["From"] = "adresse_validée@mailjet.com"

