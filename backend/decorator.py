from functools import wraps
from flask import jsonify, request, Response, g
from backend.db import get_db_connection
import jwt

# ⚠️ À sécuriser avec une vraie variable d’environnement en production
SECRET_KEY = "votre_clé_secrète"

def db_operation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Appel de la fonction décorée avec le curseur
            result = f(cursor, *args, **kwargs)

            # Commit de la transaction si tout s’est bien passé
            print("[DEBUG] Commit de la transaction")
            conn.commit()

            # Cas : la fonction retourne directement une réponse Flask
            if isinstance(result, Response):
                return result

            # Cas : retour tuple (dictionnaire, status)
            if isinstance(result, tuple) and len(result) == 2:
                data, status = result
                if isinstance(data, Response):
                    return data
                return jsonify(data), status

            # Cas : dictionnaire simple
            return jsonify(result)

        except Exception as e:
            if conn:
                print("[DEBUG] Rollback de la transaction à cause de :", str(e))
                conn.rollback()
            return jsonify({'error': str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return decorated_function


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return jsonify({"message": "Non authentifié"}), 401

        try:
            # Décodage du token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user_id = payload.get("user_id")

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Session expirée, veuillez vous reconnecter."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token invalide."}), 401

        return f(*args, **kwargs)

    return decorated
