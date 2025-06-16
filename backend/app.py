from flask import Flask
from flask_cors import CORS
from backend.routes.auth import auth
from backend.routes.immatriculation import immatriculation
from backend.routes.reservation import reservation

import os
import logging

# ✅ Logger CORS pour aider au debug
logging.getLogger('flask_cors').level = logging.DEBUG

# Définition des chemins absolus pour les certificats
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
cert_path = os.path.join(BASE_DIR, 'cert', 'cert.pem')
key_path = os.path.join(BASE_DIR, 'cert', 'key.pem')

print("Chemin absolu cert.pem :", cert_path)
print("Chemin absolu key.pem :", key_path)

app = Flask(__name__)

# ✅ Configuration CORS complète et précise
CORS(app,
     origins=[
         "https://localhost:5173",
         "https://127.0.0.1:5173"
     ],
     supports_credentials=True,
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "OPTIONS"])

# Enregistrement des routes
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(immatriculation, url_prefix='/immatriculation')
app.register_blueprint(reservation, url_prefix='/reservation')

# Route d'accueil
@app.route('/')
def index():
    return "Bienvenue sur l'API de gestion des réservations !"

@app.route('/health')
def health_check():
    return "L'API est en bonne santé !", 200

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return {"error": "Page non trouvée"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Erreur interne du serveur"}, 500

# Lancement de l'application Flask en HTTPS
if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5080,
        debug=True,
        ssl_context=(cert_path, key_path)
    )

