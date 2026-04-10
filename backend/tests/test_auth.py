import pytest
from app import User
from werkzeug.security import check_password_hash, generate_password_hash


def test_user_creation():
    """Test user creation with password hashing"""
    password = 'testpassword'
    hashed = generate_password_hash(password)
    user = User(username='testuser', password=hashed)

    assert user.username == 'testuser'
    assert check_password_hash(user.password, password)


def test_password_verification():
    """Test password verification"""
    password = 'mypassword'
    hashed = generate_password_hash(password)

    assert check_password_hash(hashed, password)
    assert not check_password_hash(hashed, 'wrongpassword')


def test_user_loader():
    """Test user loader function"""
    from app import load_user

    # This would need a proper test database setup
    # For now, just test that the function exists
    assert callable(load_user)