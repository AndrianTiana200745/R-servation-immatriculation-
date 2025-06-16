# routes/immatriculation.py
from flask import Blueprint, request
from backend.decorator import db_operation

immatriculation = Blueprint('immatriculation', __name__, url_prefix='/immatriculation')

@immatriculation.route('/disponible', methods=['GET'])
@db_operation
def get_disponibles(cursor):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    search = request.args.get('search', '').strip()

    offset = (page - 1) * limit

    base_query = """
        SELECT i.id, i.numero, c.designation AS centre, s.code AS serie
        FROM Immatriculation i
        JOIN Centre c ON i.centre_id = c.id
        JOIN Serie s ON i.serie_id = s.id
        WHERE i.est_reserve = FALSE
    """
    params = []

    if search:
        base_query += " AND i.numero LIKE %s"
        params.append(f"%{search}%")

    count_query = f"SELECT COUNT(*) as total FROM ({base_query}) AS count_table"
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']

    paginated_query = base_query + " ORDER BY i.id LIMIT %s OFFSET %s"
    params += [limit, offset]
    cursor.execute(paginated_query, params)
    rows = cursor.fetchall()

    return {
        "data": rows,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }
