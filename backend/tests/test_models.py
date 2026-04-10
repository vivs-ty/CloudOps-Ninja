import pytest
from app import db, User, Server, Deployment


def test_user_model():
    """Test User model"""
    user = User(username='testuser', password='hashedpass')
    assert user.username == 'testuser'
    assert user.password == 'hashedpass'


def test_server_model():
    """Test Server model"""
    server = Server(cloud='aws', count=3, status='healthy', cpu=50, memory=60)
    assert server.cloud == 'aws'
    assert server.count == 3
    assert server.status == 'healthy'
    assert server.cpu == 50
    assert server.memory == 60


def test_deployment_model():
    """Test Deployment model"""
    from datetime import datetime
    deployment = Deployment(cloud='aws', version='1.0.0', status='success')
    assert deployment.cloud == 'aws'
    assert deployment.version == '1.0.0'
    assert deployment.status == 'success'
    # Timestamp is set on commit, so just check it's initially None
    assert deployment.timestamp is None