from flask import Blueprint
import datetime

from models import db, Patient


api = Blueprint('api', __name__, url_prefix='')


@api.route('/api_setup_test')
def setup_test():
    return 'blueprint registered'


@api.route('/api_db_test')
def db_test():
    before = len(Patient.query.all())
    np = Patient(first_name='Bill', last_name='Gates', middle_name='Nerd', date_of_birth=datetime.datetime.now().date(),
                 external_id='1')
    db.session.add(np)
    db.session.commit()
    after = len(Patient.query.all())
    return str(before == after - 1)
