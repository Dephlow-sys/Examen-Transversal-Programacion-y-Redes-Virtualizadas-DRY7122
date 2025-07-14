import sqlite3
from flask import Flask, request, redirect, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

# === CONFIGURACIÓN INICIAL ===
# Integrantes del grupo
usuarios_validos = {
    "sura": generate_password_hash("claveSura"),
    "sandoval": generate_password_hash("claveSandoval"),
    "abarca": generate_password_hash("claveAbarca")
}

# === CREAR BASE DE DATOS Y TABLA ===
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT PRIMARY KEY,
        hash TEXT NOT NULL
    )
''')

# Insertar usuarios (si no existen)
for nombre, hashpass in usuarios_validos.items():
    cursor.execute('INSERT OR IGNORE INTO usuarios (nombre, hash) VALUES (?, ?)', (nombre, hashpass))
conn.commit()
conn.close()

# === APLICACIÓN FLASK ===
app = Flask(__name__)

html_formulario = '''
    <h2>Login Examen DRY7122</h2>
    <form method="post">
        Usuario: <input type="text" name="usuario"><br>
        Contraseña: <input type="password" name="clave"><br>
        <input type="submit" value="Ingresar">
    </form>
    <p>{{ mensaje }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario = request.form['usuario'].lower()
        clave = request.form['clave']

        # Buscar usuario en la base
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT hash FROM usuarios WHERE nombre = ?', (usuario,))
        fila = cursor.fetchone()
        conn.close()

        if fila and check_password_hash(fila[0], clave):
            mensaje = f"¡Bienvenido {usuario.title()}!"
        else:
            mensaje = "Credenciales incorrectas"

    return render_template_string(html_formulario, mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7500)

