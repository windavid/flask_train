from flask import Flask
import pathlib
import json

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


def import_json(table_name, json_name):
    table = db.metadata.tables[table_name]
    json_path = pathlib.Path(json_name)
    with json_path.open(mode='r') as f:
        json_data = json.load(f)
    for j in json_data:
        inst = table.from_json(j)
        db.session.add(inst)
    db.session.commit()


def embed():
    app = create_app()
    with app.app_context():
        from IPython import embed
        embed()


if __name__ == "__main__":
    embed()
    # app = create_app()
    # app.run()
