import mysql.connector
from mysql.connector import Error

class MariaDBConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✅ Conexión exitosa a MariaDB")
                return True
        except Error as e:
            print(f"❌ Error al conectar a MariaDB: {e}")
            return False
    
    def execute_query(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            print(f"✅ Consulta ejecutada: {query} con {params}")
            return cursor.rowcount
        except Exception as e:
            print(f"❌ Error en consulta: {e}")
            if self.connection:
                self.connection.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión a MariaDB cerrada")