import pytest
import sys
import os
sys.path.append(".")
from asset_app import app


@pytest.fixture
def client():
    app.config["LOGIN_DISABLED"] = True
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['WTF_CSRF_METHODS'] = []
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['MYSQL_USER'] + ":" + os.environ[
    'MYSQL_PASSWORD'] + "@localhost:" + os.environ['MYSQL_PORT'] + "/" + os.environ[
                                            'MYSQL_DATABASE']
    with app.test_client() as client:
        with app.app_context():
            yield client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password,
        submit='Sign In',
        form=""),
        follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def home(client):
    return client.get('/list-assets', follow_redirects=True)


def add_asset(client, assetName, assetOwner, assetDescription, assetLocation, assetCriticality):
    return client.post('/add-asset', data=dict(
        assetName=assetName,
        assetOwner=assetOwner,
        assetDescription=assetDescription,
        assetLocation=assetLocation,
        assetCriticality=assetCriticality,
        submit='Add Asset',
        form=""),
        follow_redirects=True)


def edit_asset(client, assetName, assetOwner, assetDescription, assetLocation, assetCriticality, submit_update, submit_delete):
    test_asset_id = 601
    return client.post('/edit-asset', query_string=dict(asset_id=test_asset_id), data=dict(
        assetID=test_asset_id,
        assetName=assetName,
        assetOwner=assetOwner,
        assetDescription=assetDescription,
        assetLocation=assetLocation,
        assetCriticality=assetCriticality,
        submit_update=submit_update,
        submit_delete=submit_delete,
        form=""),
        follow_redirects=True)


def get_all_assets(client):
    return client.get('/list-assets', follow_redirects=True)


def test_login_logout(client):
    """Test login and logout"""

    username = 'admin'
    password = 'password'

    rv = login(client, username, password)
    assert b'Total Assets' in rv.data

    rv = logout(client)
    assert b'Welcome Back!' in rv.data

    rv = login(client, f"{username}x", password)
    print(rv.data)
    assert b'Incorrect username or password' in rv.data

    rv = login(client, username, f'{password}x')
    assert b'Incorrect username or password' in rv.data


def test_assets(client):
    """Test asset operations"""

    assetName = 'test_asset_1'
    assetOwner = 'test_owner_1'
    assetDescription = 'test_description'
    assetLocation = 'test_location'
    assetCriticality = 'low'

    # Get all assets
    rv = get_all_assets(client)
    assert b'test_asset_1' not in rv.data
    assert b'test_asset_1' not in rv.data
    assert b'Samsung 201945' in rv.data

    # Add asset
    rv = add_asset(client, assetName, assetOwner,
                   assetDescription, assetLocation, assetCriticality)
    assert b'test_asset_1' in rv.data
    assert b'test_owner_1' in rv.data

    # Edit asset
    assetName = 'test_asset_2'
    assetOwner = 'test_owner_2'
    rv = edit_asset(client, assetName, assetOwner, assetDescription,
                    assetLocation, assetCriticality, "Update Asset", "")
    assert b'test_asset_2' in rv.data
    assert b'test_owner_2' in rv.data
    assert b'test_asset_1' not in rv.data
    assert b'test_owner_1' not in rv.data

    # Delete asset
    rv = edit_asset(client, assetName, assetOwner, assetDescription,
                    assetLocation, assetCriticality, "", "Delete Asset")
    assert b'test_asset_2' not in rv.data
    assert b'test_owner_2' not in rv.data
    assert b'test_asset_1' not in rv.data
    assert b'test_owner_1' not in rv.data
