from flask import Flask
from models import db



def create_app():
    # TODO: configure app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aspdfiojapfiha'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # TODO: ssl

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
