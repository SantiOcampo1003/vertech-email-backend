import pytest
from ..app import create_app
from ..database.db import db


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_user_registration_with_valid_credentials(client):
    # Create a new user
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 201
    assert 'message' in response.json


def test_duplicate_user_registration(client):
    # Register the same user twice
    client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 400
    assert 'message' in response.json
    assert response.json['message'] == 'Username already exists.'


def test_user_login_with_valid_credentials(client):
    # Register a user
    client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    # Login with correct credentials
    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_with_invalid_credentials(client):
    # Attempt login with incorrect credentials
    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401
    assert 'message' in response.json
    assert response.json['message'] == 'Invalid credentials.'
