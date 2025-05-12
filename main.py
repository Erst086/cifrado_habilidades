import string
from flask import Flask, render_template, jsonify, request
from conexion import MariaDBConnection

app = Flask(__name__)

def cifrar_mensaje(mensaje):
    cifrado = ""
    for letra in mensaje:
        if letra in string.ascii_letters:
            idx = string.ascii_letters.find(letra)
            new_idx = (idx + 3) % len(string.ascii_letters)
            cifrado += string.ascii_letters[new_idx]
        else:
            cifrado += letra
    return cifrado

def decifrar(mensaje):
    cifrado = ""
    for letra in mensaje:
        if letra in string.ascii_letters:
            idx = string.ascii_letters.find(letra)
            new_idx = (idx - 3) % len(string.ascii_letters)
            cifrado += string.ascii_letters[new_idx]
        else:
            cifrado += letra
    return cifrado

def get_connection():
    try:
        connection = MariaDBConnection(
            host='localhost',
            user='root',
            password='312908', ##319192142
            database='cifrado'
        )
        connection.connect()
        if not connection.connection or not connection.connection.is_connected():
            raise Exception("No se pudo conectar a la base de datos")
        return connection
    except Exception as e:
        print(f"Error al obtener conexión: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cifrar', methods=['POST'])
def cifrar():
    data = request.json
    if not data or 'mensaje' not in data:
        return jsonify({'status': 'error', 'message': 'Datos inválidos'}), 400
        
    mensaje = data.get('mensaje', '')[:30]
    cifrado = cifrar_mensaje(mensaje)

    conn = None
    try:
        conn = get_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Error de conexión a BD'}), 500
            
        query = "INSERT INTO mensajes (palabra, cifrado) VALUES (%s, %s)"
        rows_affected = conn.execute_query(query, (mensaje, cifrado))
        
        if rows_affected == 0:
            return jsonify({'status': 'error', 'message': 'No se insertaron filas'}), 500
            
        cursor = conn.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mensajes ORDER BY id DESC LIMIT 1")
        last_record = cursor.fetchone()
        cursor.close()
        
        print(f"Registro insertado: {last_record}")
        
        return jsonify({
            'cifrado': cifrado,
            'status': 'success',
            'inserted_id': last_record['id'] if last_record else None
        })
    except Exception as e:
        print(f"Error en operación de BD: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if conn:
            conn.disconnect()

if __name__ == "__main__":
    app.run('0.0.0.0', 8888, debug=True)