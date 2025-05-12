import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='319192142',
            database='cifrado'
        )
        print("✅ Conexión exitosa a la base de datos")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    test_connection()