import pytest

from models import db
from mapp import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def _db(app):
    """
    return an empty database
    database is created on disk, it will be dropped after tests, no changes will be saved
    """
    # TODO: don't drop if db is empty
    db.drop_all()
    db.create_all()
    yield db
    db.drop_all()
