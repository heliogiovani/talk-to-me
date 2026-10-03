from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registo dos Controllers (Blueprints)
    from app.controllers.card_controller import card_bp
    app.register_blueprint(card_bp)

    # Rota da View principal
    @app.route('/')
    def index():
        return render_template('index.html')

    return app