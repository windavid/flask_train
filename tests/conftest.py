import pytest

from models import db
from mapp import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def _db(app):
    return db
