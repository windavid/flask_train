import pytest

from mapp import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def _db(app):
    from mapp import db
    return db
