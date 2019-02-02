import datetime
import copy
from jsonschema import validate
import pytest
import sqlalchemy.exc
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


def test_patients(_db):
    # json, create & update time
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
    assert pat.updated >= mod_time
    assert pat.to_json() == {
        "firstName": "Rick Junior",
        "lastName": "Deckard",
        "dateOfBirth": "2094-02-01",
        "externalId": "5"
    }


def test_payments(_db):
    now = datetime.datetime.utcnow()
    pay = Payment.from_json({
        "amount": 4.46,
        "patientId": "5",
        "externalId": "501"
    })
    assert pay.id is None
    _db.session.add(pay)
    _db.session.commit()
    assert pay.id > 0
    assert pay.created >= now
    assert pay.created == pay.updated

    mod_time = datetime.datetime.utcnow()
    pay.amount += 1.0
    _db.session.commit()
    assert pay.updated >= mod_time

    assert pay.to_json() == {
        "amount": 5.46,
        "patientId": "5",
        "externalId": "501"
    }


def test_unique_external(_db):
    pay_json = {
        "amount": 4.46,
        "patientId": "5",
        "externalId": "501"
    }
    for _ in range(2):
        _db.session.add(Payment.from_json(copy.copy(pay_json)))
    with pytest.raises(sqlalchemy.exc.IntegrityError) as excinfo:
        _db.session.commit()
        assert 'UNIQUE constraint failed: payments.external_id' in excinfo.value.message
    _db.session.rollback()

    pat_json = {
        "firstName": "Rick",
        "lastName": "Deckard",
        "dateOfBirth": "2094-02-01",
        "externalId": "5"
    }
    for _ in range(2):
        _db.session.add(Patient.from_json(copy.copy(pat_json)))
    with pytest.raises(sqlalchemy.exc.IntegrityError) as excinfo:
        _db.session.commit()
        assert 'UNIQUE constraint failed: patients.external_id' in excinfo.value.message


def test_patient_filter(_db):
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
    }, {
        "firstName": "Roy",
        "lastName": "Batti",
        "dateOfBirth": "2093-06-12",
        "externalId": "8"
    }]
    payments = [{
        "amount": 10,
        "patientId": "1",
        "externalId": "501"
    }, {
        "amount": 10,
        "patientId": "1",
        "externalId": "502"
    }, {
        "amount": 10,
        "patientId": "2",
        "externalId": "503"
    }]
    for p in patients:
        _db.session.add(Patient.from_json(p))
    for p in payments:
        _db.session.add(Payment.from_json(p))
    _db.session.commit()
    q0 = Patient.query.filter(Patient.payments_sum > 15).all()
    assert len(q0) == 1
    assert q0[0].first_name == "Rick"
    q1 = Patient.query.filter(Patient.payments_sum < 15).filter(Patient.payments_sum > 5).all()
    assert len(q1) == 1
    assert q1[0].first_name == "Pris"
    q2 = Patient.query.filter(Patient.payments_sum < 5).all()
    assert len(q2) == 1
    assert q2[0].first_name == "Roy"
