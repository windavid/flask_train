import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseMixin:
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.DateTime)
    updated = sa.Column(sa.DateTime)


class Patient(db.Model, BaseMixin):
    __tablename__ = 'patients'

    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String)
    date_of_birth = sa.Column(sa.Date)
    external_id = sa.Column(sa.String)  # shouldn't it be unique?


class Payment(db.Model, BaseMixin):
    __tablename__ = 'payments'

    amount = sa.Column(sa.Float, nullable=False)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('patients.id'), nullable=False)
    external_id = sa.Column(sa.String)

