from flask import Flask
import pathlib
import json

from models import db


def create_app(dbname, drop_table=False):
    # TODO: pass configuration instead of dbname and drop_table
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aspdfiojapfiha'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbname}'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # TODO: ssl

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


def import_json(table_name, json_name):
    from models import models

    model = models[table_name]
    print(f"import '{json_name}' to '{table_name}' table")
    before_entries = model.query.count()
    print(f"before import table contains {before_entries} entries")
    json_path = pathlib.Path(json_name)
    with json_path.open(mode='r') as f:
        json_data = json.load(f)
    print(f"importing {len(json_data)} entries")
    for j in json_data:
        inst = model.from_json(j)
        db.session.add(inst)
    db.session.commit()
    after_entries = model.query.count()
    print(f"after import table contains {after_entries} entries")
