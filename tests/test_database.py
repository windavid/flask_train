import datetime
from jsonschema import validate
import pytest

import schemas
from models import Patient, Payment


def test_schemas():
    patients = [{
        "firstName": "Rick",
        "lastName": "Deckard",
        "dateOfBirth": "2094-02-01",
        "externalId": "5"
    }, {
        "firstName": "Pris",
        "lastName": "Stratton",
        "dateOfBirth": "2093-12-20",
        "externalId": "4"
    }]
    payments = [{
        "amount": 4.46,
        "patientId": "5",
        "externalId": "501"
    }, {
        "amount": 5.66,
        "patientId": "5",
        "externalId": "502"
    }]
    # TODO: use fast json instead
    validate(patients, schemas.patient_arr)
    validate(payments, schemas.payment_arr)
    # TODO: assert raises checks (incorrect jsons)


def test_json_translations(_db):
    now = datetime.datetime.utcnow()
    pat = Patient.from_json({
        "firstName": "Rick",
        "lastName": "Deckard",
        "dateOfBirth": "2094-02-01",
        "externalId": "5"
    })
    assert pat.id is None
    _db.session.add(pat)
    _db.session.commit()
    assert pat.id > 0
    assert pat.created >= now

    mod_time = datetime.datetime.utcnow()
    pat.first_name += " Junior"
    _db.session.commit()

    assert pat.updated > mod_time
