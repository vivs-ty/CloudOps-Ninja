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
    with client.application.app_context():
        # Log in the test user
        from flask_login import login_user
        test_user = User.query.filter_by(username='testuser').first()
        login_user(test_user)

    return client