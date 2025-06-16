import jwt
import requests
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from backend.decorator import db_operation
import bcrypt
import mysql.connector

SECRET_KEY = "votre_clé_secrète"  # 🔐 à sécuriser
MAILBOXLAYER_KEY = "c927441d0bb9fde3d46e1a208bdb3dee"  # 🔐 à sécuriser

auth = Blueprint('auth', __name__)

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def set_token_cookie(resp, token):
    resp.set_cookie("token", token, httponly=True, secure=True, samesite="Lax")

def verifier_email(email):
    url = f"https://apilayer.net/api/check?access_key={MAILBOXLAYER_KEY}&email={email}&smtp=1&format=1"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("format_valid") and data.get("mx_found") and data.get("smtp_check")
    except Exception as e:
        print("[DEBUG] Erreur vérification email :", str(e))
        return False

@auth.route('/register', methods=['POST'])
@db_operation
def register(cursor):
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'utilisateur')

    if role not in ['utilisateur', 'admin']:
        role = 'utilisateur'

    if not verifier_email(email):
        return jsonify({"error": "Adresse e-mail invalide ou injoignable"}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute(
            "INSERT INTO Utilisateur (nom, prenom, email, password, role) VALUES (%s, %s, %s, %s, %s)",
            (nom, prenom, email, password_hash, role)
        )
        print("[DEBUG] Insert effectué, lastrowid =", cursor.lastrowid)

        # commit explicite ici au cas où le décorateur aurait un souci
        #cursor.connection.commit()

        user_id = cursor.lastrowid
        token = generate_token(user_id)

        resp = make_response({"message": "Inscription réussie"})
        set_token_cookie(resp, token)
        return resp, 201
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1062:
            return jsonify({"error": "Email déjà utilisé"}), 409
        return jsonify({"error": "Erreur serveur"}), 500

@auth.route('/login', methods=['POST'])
@db_operation
def login(cursor):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT id, password FROM Utilisateur WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    user_id, password_hash = user['id'], user['password']
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    token = generate_token(user_id)
    resp = make_response({"message": "Connexion réussie"})
    set_token_cookie(resp, token)
    return resp, 200

@auth.route('/logout', methods=['POST'])
def logout():
    resp = make_response({"message": "Déconnexion réussie"})
    resp.set_cookie("token", "", expires=0, httponly=True, secure=True, samesite="Lax")
    return resp, 200
