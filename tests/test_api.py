from flask import url_for


def test_blueprint_setup(client):
    r = client.get(url_for('api.setup_test'))
    assert r.status_code == 200
    assert b'blueprint registered' in r.data


def test_database(client, _db):
    r = client.get(url_for('api.db_test'))
    assert b'True' in r.data


# test for payments

# test for patients