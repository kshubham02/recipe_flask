from .models import User, Recipe
from . import create_app, db
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch
from flask import url_for
from flask_login import current_user
from flask_restful import Resource
from flask_login import login_required
import pytest



@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  
        "SERVER_NAME": "localhost",
        "APPLICATION_ROOT": "/",
        "PREFERRED_URL_SCHEME": "http"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user_success(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    
    assert response.status_code == 201
    json_data = response.get_json()
    
    assert json_data['message'] == 'User registered successfully'
    assert json_data['username'] == 'testuser'
    assert json_data['email'] == 'test@example.com'
    assert 'id' in json_data

    # Verify user exists in the database
    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.check_password('password')

