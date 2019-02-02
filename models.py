import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
import datetime
from jsonschema import validate
import schemas


db = SQLAlchemy()


class BaseMixin:
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    updated = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    _from_json_translate = {}  # {"javaStyleName": "python_style_name", ...}
    _json_schema = None        # a link to a schemas's jsonschema dict

    @classmethod
    def from_json(cls, jdict):
        # TODO: use python-fastjsonschema
        if cls._json_schema:
            validate(jdict, cls._json_schema)
        for key1, key2 in cls._from_json_translate.items():
            jdict[key2] = jdict.pop(key1)
        return cls(**jdict)

    def to_json(self):
        return {key1: getattr(self, key2) for key1, key2 in self._from_json_translate.items()}


class Patient(db.Model, BaseMixin):
    __tablename__ = 'patients'

    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String)
    date_of_birth = sa.Column(sa.Date)
    external_id = sa.Column(sa.String)  # shouldn't it be unique?

    # TODO: find a plugin to do it
    _from_json_translate = {'externalId': 'external_id', "firstName": "first_name", "lastName": "last_name",
                            "dateOfBirth": "date_of_birth"}
    _json_schema = schemas.patient

    @classmethod
    def from_json(cls, jdict):
        if cls._json_schema:
            validate(jdict, cls._json_schema)
        for key1, key2 in cls._from_json_translate.items():
            jdict[key2] = jdict.pop(key1)
        jdict['date_of_birth'] = datetime.datetime.strptime(jdict['date_of_birth'], "%Y-%m-%d").date()
        return cls(**jdict)

    def to_json(self):
        d = super().to_json()
        d['dateOfBirth'] = datetime.datetime.strftime(d['dateOfBirth'], "%Y-%m-%d")
        return d


class Payment(db.Model, BaseMixin):
    __tablename__ = 'payments'

    amount = sa.Column(sa.Float, nullable=False)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('patients.id'), nullable=False)
    external_id = sa.Column(sa.String)

    _from_json_translate = {'patientId': 'patient_id', 'externalId': 'external_id'}
    _json_schema = schemas.payment

    @classmethod
    def from_json(cls, jdict):
        if cls._json_schema:
            validate(jdict, cls._json_schema)
        for key1, key2 in cls._from_json_translate.items():
            jdict[key2] = jdict.pop(key1)
        jdict['patient_id'] = int(jdict['patient_id'])
        return cls(**jdict)

    def to_json(self):
        d = super().to_json()
        d['patientId'] = str(d['patientId'])
        d['amount'] = self.amount
        return d
