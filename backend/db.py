import mysql.connector
from mysql.connector import pooling

class Connection:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if self._instance is not None:
            raise RecursionError("La connection est interompue car ceci est un singleton.")
        else:
            self.connection_pool = self._create_pool()
    
    def _create_pool(self):
        config = {
            'user': 'andrian',
            'password': 'tonmotdepasse',
            'host': 'localhost',
            'database': 'reservations',
            'pool_name': 'reservations_pool',
            'pool_size': 5
        }
        return mysql.connector.pooling.MySQLConnectionPool(**config)
    def get_connection(self):
        try:
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                return connection
        except mysql.connector.Error as err:
            print(f"Erreur de connexion à la base de données: {err}")
            return None
    
def get_db_connection():
    return Connection.get_instance().get_connection()
    