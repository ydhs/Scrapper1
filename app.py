from flask import Flask
from api import api_blueprint
from flask_cors import CORS
# from web import web_blueprint  #  позже

app = Flask(__name__)
CORS(app)  # устранение проблемы с внешними запросами
app.register_blueprint(api_blueprint, url_prefix="/api")
# app.register_blueprint(web_blueprint, url_prefix="/web")  # будущая интеграция большого веб

if __name__ == "__main__":
    app.run(debug=True)
