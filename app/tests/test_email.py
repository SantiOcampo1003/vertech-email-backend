import pytest
from ..app import create_app
from ..database.db import db
from flask_jwt_extended import create_access_token

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

def test_send_email(client):
    response_sender = client.post(
        '/api/register',
        json={'name': 'Sender User', 'u_email': 'sender@example.com', 'password': 'test123'}
    )
    assert response_sender.status_code == 201

    response_recipient = client.post(
        '/api/register',
        json={'name': 'Recipient User', 'u_email': 'recipient@example.com', 'password': 'test123'}
    )
    assert response_recipient.status_code == 201

    response_login = client.post(
        '/api/login',
        json={'u_email': 'sender@example.com', 'password': 'test123'}
    )
    assert response_login.status_code == 200
    access_token = response_login.json['access_token']

    response_send_email = client.post(
        '/api/emails',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'recipient_email': 'recipient@example.com', 'subject': 'Test Subject', 'body': 'Test Body'}
    )
    assert response_send_email.status_code == 201
     

def test_get_emails(client):

    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 201

    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 200
    access_token = response.json['access_token']

    response = client.get(
        '/api/emails',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)
    

def test_get_email_detail(client):
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 201

    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 200
    access_token = response.json['access_token']

    response = client.get(
        '/api/emails/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 404

def test_get_users(client):
    response = client.post(
        '/api/register',
        json={'name': 'Test User', 'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 201

    response = client.post(
        '/api/login',
        json={'u_email': 'test@example.com', 'password': 'test123'}
    )
    assert response.status_code == 200
    access_token = response.json['access_token']
    response = client.get('/api/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0


    