from sqlalchemy.orm import Session
from app.models import User


def test_update_user_email_already_exists(client):
    response = client.put(
        "/users/update/1",
        json={
            "username": "newname",
            "email": "existing@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"].lower() == "Email belongs to another user.".lower()
    assert response.headers["x-error-code"] == "EMAIL_TAKEN"


def test_update_user_not_found(client):
    response = client.put(
        "/users/update/9999",
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"].lower() == "user Not Found.".lower()
    assert response.headers["x-error-code"] == "USER_NOT_FOUND"

def test_update_user_success(client):
    response = client.put(
        "/users/update/1",
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user"]['username'] == "test"
    assert data['user']["email"] == "test@test.com"


def test_get_all_users(client):
    response = client.get('/users')

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert 'username' in data[0]
    assert 'email' in data[0]

def test_get_user_not_found(client):
    response = client.get('/users/get/9999')

    assert response.status_code == 404
    assert response.json()["detail"].lower() == "user Not Found.".lower()
    assert response.headers["x-error-code"] == "USER_NOT_FOUND"

def test_get_user_success(client):
    response = client.get('/users/get/1')

    assert response.status_code == 200
    data = response.json()
    assert data['user']['id'] == 1
    assert 'username' in data['user']
    assert 'email' in data['user']

def test_create_user_username_or_email_taken(client):
    response = client.post(
        '/users/create',
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "123456"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"].lower() == "Username Or Email already registered.".lower()
    assert response.headers["x-error-code"] == "USERNAME_OR_EMAIL_TAKEN"

def test_create_user_invalid_username(client):
    response = client.post(
        '/users/create',
        json={
            "username": "admin",
            "email": "admin@admin.com",
            "password": "123456"
        })

    assert response.status_code == 400
    assert response.json()["detail"].lower() == "Username 'admin' is not allowed.".lower()
    assert response.headers["x-error-code"] == "INVALID_USERNAME"

def test_create_user_success(client, db: Session):
    response = client.post(
        "/users/create",
        json={
            "username": "newuser",
            "email": "user@user.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "user@user.com"

    user = db.get(User, data["user"]["id"])
    db.delete(user)
    db.commit()

def test_user_login_invalid_credentials(client):
    response = client.post(
        '/users/login',
        data={
            "username": "wronguser",
            "password": "wrongpass"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 401
    assert response.json()["detail"].lower() == "Invalid credentials.".lower()
    assert response.headers["x-error-code"] == "INVALID_CREDENTIALS"

def test_user_login_success(client, db: Session):
    response = client.post(
        '/users/login',
        data={
            "username": "test",
            "password": "123456"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_profile_success(client):
    response = client.get(
        '/profile',
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzY1ODg3OTM1fQ.Pn0UoKm-sLInBose0pxxZ9rldQzt-mT2WiXhTuU235Q"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "test"
    assert data["user"]["email"] == "test@test.com"
