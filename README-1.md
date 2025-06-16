# 🚗 Réservation Immatriculation

Une application web complète pour gérer la réservation d'immatriculations dans des centres d'immatriculation. Le projet est basé sur un backend **Flask** (Python) avec base de données **MySQL**, et un frontend **React** moderne.

## ✨ Fonctionnalités

- Authentification des utilisateurs (inscription, connexion)
- Visualisation des immatriculations disponibles
- Réservation d’une immatriculation
- Génération automatique d’immatriculations et de séries
- Interface utilisateur simple et responsive
- Intégration SSL pour les connexions sécurisées

---

## 📁 Architecture du projet

```
R-servation-immatriculation-/
├── backend/              # Serveur Flask
│   ├── cert/             # Certificats SSL locaux
│   ├── db.py             # Connexion MySQL
│   ├── decorator.py      # Décorateur pour la BDD
│   ├── main.py           # Point d'entrée Flask
│   └── routes/           # Routes organisées par fonctionnalité
│       ├── auth.py
│       ├── immatriculation.py
│       └── reservation.py
├── frontend/             # Application React
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── App.jsx
│       └── main.jsx
└── README.md
```

---

## 🧰 Technologies utilisées

### Backend
- Python 3.x
- Flask
- MySQL
- bcrypt
- Flask-CORS

### Frontend
- React
- Axios
- React Router
- (Facultatif : MaterializeCSS ou autre framework CSS)

---

## ⚙️ Installation et configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/AndrianTiana200745/R-servation-immatriculation-.git
cd R-servation-immatriculation-
```

### 2. Configuration du backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Ou venv\Scripts\activate sous Windows

pip install -r requirements.txt
```

Configurer la base de données MySQL (créer les tables, procédures stockées, etc.), puis lancer :

```bash
python -m backend.app
```

### 3. Configuration du frontend (React)

```bash
cd ../frontend
npm install
npm  dev

ou yarn install 
yarn dev
```

---

## 🔒 Sécurité

- Les mots de passe sont hashés avec `bcrypt`.
- Connexions sécurisées avec certificats SSL en développement.
- Prévoir une vérification d’email via une API tierce (ex. : Mailboxlayer).

---

## 🛠️ Fonctionnalités à améliorer / TODO

- ✅ Ajout de la pagination côté React
- ✅ Système de réservation et génération automatique
- 🔲 Validation de l'email à l'inscription
- 🔲 Affichage de l’historique de réservation
- 🔲 Tests unitaires backend
- 🔲 Dockerisation du projet

---

## 📄 Licence

Ce projet est open-source et libre d’utilisation pour tout usage académique ou personnel.  
(Merci de mentionner l’auteur si vous l’utilisez dans un autre contexte.)

---

## 👨‍💻 Auteur

Développé par **Tiana Razafindrakoto**  
🔗 [GitHub](https://github.com/AndrianTiana200745)
