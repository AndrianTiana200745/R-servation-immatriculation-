from flask import Blueprint, request, g
from backend.decorator import db_operation, auth_required
from datetime import datetime

reservation = Blueprint('reservation', __name__, url_prefix='/reservation')

@reservation.route('/creer', methods=['POST'])
@auth_required  # ✅ d'abord vérifier l'authentification
@db_operation   # ✅ ensuite accéder à la DB
def reserver(cursor):
    data = request.get_json()
    immatriculation_id = data.get('immatriculation_id')
    utilisateur_id = g.user_id  # ✅ récupéré du token

    if not immatriculation_id:
        return {'message': 'Champ immatriculation manquant'}, 400

    # Vérifie si déjà réservée
    cursor.execute("SELECT est_reserve FROM Immatriculation WHERE id = %s", (immatriculation_id,))
    row = cursor.fetchone()
    if not row or row['est_reserve']:
        return {'message': 'Immatriculation déjà réservée ou introuvable'}, 400

    # Création de la réservation
    cursor.execute("""
        INSERT INTO Reservation (utilisateur_id, immatriculation_id, date_reservation, statut)
        VALUES (%s, %s, %s, 'en attente')
    """, (utilisateur_id, immatriculation_id, datetime.now()))

    # Marquer comme réservée
    cursor.execute("UPDATE Immatriculation SET est_reserve = TRUE WHERE id = %s", (immatriculation_id,))

    return {'message': 'Réservation effectuée avec succès'}
