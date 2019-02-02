from flask import Flask
import pathlib
import json
import datetime

from models import db


def create_app(dbname, drop_table=False):
    # TODO: pass configuration instead of dbname and drop_table
    # TODO: nginx, not werkzeug
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
    # TODO: unit test
    from models import models

    model = models[table_name]
    print(f"import '{json_name}' to '{table_name}' table")
    before_entries = model.query.count()
    print(f"before import table contains {before_entries} entries")
    json_path = pathlib.Path(json_name)
    with json_path.open(mode='r') as f:
        json_data = json.load(f)
    print(f"importing {len(json_data)} entries")
    # if something not in json, it was deleted on remote
    # can not drop the table and fill it again, because it will break create and update fields
    # use update value for now
    # TODO: if incorrect, add extra bool sync flag
    sync_start = datetime.datetime.utcnow()
    for j in json_data:
        inst = model.query.filter(model.external_id == j["externalId"]).first()
        if not inst:
            inst = model.from_json(j)
        else:
            j.pop("externalId")
            for k, v in j.items():
                setattr(inst, k, v)
            inst.updated = datetime.datetime.utcnow()
        db.session.add(inst)
    db.session.commit()
    # remove values that were not updated
    model.query.filter(model.updated < sync_start).delete()

    after_entries = model.query.count()
    print(f"after import table contains {after_entries} entries")
