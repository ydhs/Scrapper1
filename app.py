import os
import json

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_cors import CORS
from api import api_blueprint
from web import web_blueprint

# Загрузка auth.json
if not os.path.exists("auth.json"):
    raise RuntimeError("Файл auth.json не найден. Создайте его рядом с app.py.")
with open("auth.json", encoding="utf-8") as f:
    auth = json.load(f)

app = Flask(__name__)
app.secret_key = auth.get("secret_key")
CORS(app)  # устранение проблемы с внешними запросами

login_manager = LoginManager(app)
login_manager.login_view = "login"
USERS = auth.get("users", {})

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

# вход
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if USERS.get(username) == password:
            login_user(User(username))
            next_page = request.args.get("next") or url_for("web.index")
            return redirect(next_page)
        flash("Неверное имя пользователя или пароль", "danger")
    return render_template("login.html")

# выход
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(web_blueprint, url_prefix="")  # будущая интеграция большого веб

if __name__ == "__main__":
    app.run(debug=True)
