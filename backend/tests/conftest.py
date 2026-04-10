import pytest
import os
import tempfile
from app import app, db, User, Server, Deployment, initialize_app_data


@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.secret_key = 'test-secret-key'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            initialize_app_data()

        yield client


@pytest.fixture
def authenticated_client(client):
    """Authenticated test client fixture"""
    # Log in via POST request
    client.post('/login', data={'username': 'admin', 'password': 'password'})
    return client