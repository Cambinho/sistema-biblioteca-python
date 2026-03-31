import psycopg2

class ConexaoDB:
    def __init__(self):
        self.config = {
            "dbname": "biblioteca_db",
            "user": "postgres",
            "password": "senacrs",
            "host": "localhost",
            "port": "5432"
        }

    def conectar(self):
        try:
            return psycopg2.connect(**self.config)
        except Exception as erro:
            print("Erro de conexão:", erro)
            return None