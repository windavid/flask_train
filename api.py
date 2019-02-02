from flask import Blueprint, jsonify
import datetime
from webargs import fields, missing
from webargs.flaskparser import use_args

from models import db, Patient, Payment


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


@api.route('/patients')
@use_args({'payment_min': fields.Int(missing=None),
           'payments_max': fields.Int(missing=None)}, locations=("query",))
def patients(args):
    # TODO: unit test
    query = Patient.query
    if args.get("payment_min"):
        query = query.filter(Patient.payments_sum >= args["payment_min"])
    if args.get("payments_max"):
        query = query.filter(Patient.payments_sum <= args["payments_max"])
    return jsonify([p.to_json() for p in query.all()])


@api.route('/payments')
@use_args({'external_id': fields.Str(missing=None)}, locations=("query",))
def payments(args):
    # TODO: unit test
    query = Payment.query
    if args.get("external_id"):
        query = query.filter(Payment.external_id == args["external_id"])
    return jsonify([p.to_json() for p in query.all()])
