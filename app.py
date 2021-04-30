from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.base_model import db
import os

api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'chat_api')

app = Flask('chat', root_path=api_dir)
app.secret_key = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)
jwt = JWTManager(app)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origin" : "*"}})


if os.getenv("FLASK_ENV") == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc