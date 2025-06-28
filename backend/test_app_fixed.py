"""
Test suite for the Mentor-Mentee Matching Application API
Tests all endpoints according to the API specification
"""

import pytest
import json
import os
import tempfile
from werkzeug.security import generate_password_hash
from app import app, db, User, MatchRequest


@pytest.fixture
def test_app():
    """Create and configure a test app"""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def test_client(test_app):
    """Create a test client"""
    return test_app.test_client()


def create_test_mentor(app):
    """Helper to create a test mentor user"""
    with app.app_context():
        user = User(
            email="mentor@test.com",
            password_hash=generate_password_hash("password123"),
            name="Test Mentor",
            role="mentor",
            bio="I am a test mentor",
            skills="Python,Machine Learning",
            availability="weekends",
        )
        db.session.add(user)
        db.session.commit()
        return user.id


def create_test_mentee(app):
    """Helper to create a test mentee user"""
    with app.app_context():
        user = User(
            email="mentee@test.com",
            password_hash=generate_password_hash("password123"),
            name="Test Mentee",
            role="mentee",
            bio="I am a test mentee",
            interests="Python,Web Development",
        )
        db.session.add(user)
        db.session.commit()
        return user.id


def get_auth_headers(client, email, password):
    """Helper to get authentication headers"""
    response = client.post(
        "/api/login",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    return {"Authorization": f'Bearer {data["token"]}'}


class TestAuthentication:
    """Test authentication endpoints"""

    def test_signup_success(self, client):
        """Test successful user signup"""
        response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "newuser@test.com",
                    "password": "password123",
                    "name": "New User",
                    "role": "mentee",
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "User created successfully"
        assert "token" in data

    def test_signup_duplicate_email(self, client, app):
        """Test signup with duplicate email"""
        # Create a user first
        create_test_mentor(app)

        response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "mentor@test.com",  # Same email
                    "password": "password123",
                    "name": "Another User",
                    "role": "mentee",
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "already exists" in data["error"]

    def test_signup_invalid_role(self, client):
        """Test signup with invalid role"""
        response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "invalid@test.com",
                    "password": "password123",
                    "name": "Invalid User",
                    "role": "invalid_role",
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Role must be" in data["error"]

    def test_login_success(self, client, app):
        """Test successful login"""
        # Create a user first
        create_test_mentor(app)

        response = client.post(
            "/api/login",
            data=json.dumps({"email": "mentor@test.com", "password": "password123"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "token" in data
        assert data["user"]["email"] == "mentor@test.com"
        assert data["user"]["role"] == "mentor"

    def test_login_invalid_credentials(self, client, app):
        """Test login with invalid credentials"""
        # Create a user first
        create_test_mentor(app)

        response = client.post(
            "/api/login",
            data=json.dumps({"email": "mentor@test.com", "password": "wrongpassword"}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert "Invalid credentials" in data["error"]


class TestProfile:
    """Test profile management endpoints"""

    def test_get_profile_mentor(self, client, app):
        """Test getting mentor profile"""
        # Create a mentor user
        create_test_mentor(app)
        headers = get_auth_headers(client, "mentor@test.com", "password123")

        response = client.get("/api/profile", headers=headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["email"] == "mentor@test.com"
        assert data["role"] == "mentor"
        assert data["name"] == "Test Mentor"

    def test_get_profile_mentee(self, client, app):
        """Test getting mentee profile"""
        # Create a mentee user
        create_test_mentee(app)
        headers = get_auth_headers(client, "mentee@test.com", "password123")

        response = client.get("/api/profile", headers=headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["email"] == "mentee@test.com"
        assert data["role"] == "mentee"
        assert data["name"] == "Test Mentee"

    def test_update_profile_mentor(self, client, app):
        """Test updating mentor profile"""
        # Create a mentor user
        create_test_mentor(app)
        headers = get_auth_headers(client, "mentor@test.com", "password123")

        response = client.put(
            "/api/profile",
            data=json.dumps(
                {
                    "name": "Updated Mentor",
                    "bio": "Updated bio",
                    "skills": "Python,AI,ML",
                    "availability": "evenings",
                }
            ),
            content_type="application/json",
            headers=headers,
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Profile updated successfully"

        # Verify the update
        response = client.get("/api/profile", headers=headers)
        data = json.loads(response.data)
        assert data["name"] == "Updated Mentor"
        assert data["bio"] == "Updated bio"

    def test_get_profile_unauthorized(self, client):
        """Test getting profile without authentication"""
        response = client.get("/api/profile")

        assert response.status_code == 401


class TestMentorListing:
    """Test mentor listing and filtering"""

    def test_get_mentors_as_mentee(self, client, app):
        """Test getting mentors list as mentee"""
        # Create a mentor and a mentee
        create_test_mentor(app)
        create_test_mentee(app)

        headers = get_auth_headers(client, "mentee@test.com", "password123")

        response = client.get("/api/mentors", headers=headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "mentors" in data
        assert len(data["mentors"]) >= 1
        assert data["mentors"][0]["role"] == "mentor"

    def test_get_mentors_with_skill_filter(self, client, app):
        """Test getting mentors with skill filter"""
        # Create a mentor and a mentee
        create_test_mentor(app)
        create_test_mentee(app)

        headers = get_auth_headers(client, "mentee@test.com", "password123")

        response = client.get("/api/mentors?skill=Python", headers=headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "mentors" in data
        # Should find the mentor with Python skills
        if len(data["mentors"]) > 0:
            assert "Python" in data["mentors"][0]["skills"]


class TestMatchingRequests:
    """Test matching request system"""

    def test_create_request_as_mentee(self, client, app):
        """Test creating match request as mentee"""
        # Create mentor and mentee
        mentor_id = create_test_mentor(app)
        create_test_mentee(app)

        headers = get_auth_headers(client, "mentee@test.com", "password123")

        response = client.post(
            "/api/match-requests",
            data=json.dumps(
                {"mentor_id": mentor_id, "message": "I would like to learn from you"}
            ),
            content_type="application/json",
            headers=headers,
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "Match request sent successfully"

    def test_create_request_as_mentor_fails(self, client, app):
        """Test that mentors cannot create match requests"""
        # Create mentor and mentee
        create_test_mentor(app)
        mentee_id = create_test_mentee(app)

        headers = get_auth_headers(client, "mentor@test.com", "password123")

        response = client.post(
            "/api/match-requests",
            data=json.dumps(
                {
                    "mentor_id": mentee_id,  # This doesn't make sense but testing the role check
                    "message": "This should fail",
                }
            ),
            content_type="application/json",
            headers=headers,
        )

        assert response.status_code == 403
        data = json.loads(response.data)
        assert "Only mentees can send match requests" in data["error"]

    def test_get_requests_as_mentee(self, client, app):
        """Test getting requests as mentee"""
        # Create users and a request
        mentor_id = create_test_mentor(app)
        create_test_mentee(app)

        headers = get_auth_headers(client, "mentee@test.com", "password123")

        # Create a request first
        client.post(
            "/api/match-requests",
            data=json.dumps({"mentor_id": mentor_id, "message": "Test request"}),
            content_type="application/json",
            headers=headers,
        )

        # Get requests
        response = client.get("/api/match-requests", headers=headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "requests" in data

    def test_get_requests_as_mentor(self, client, app):
        """Test getting requests as mentor"""
        # Create users and a request
        mentor_id = create_test_mentor(app)
        create_test_mentee(app)

        # Create request as mentee
        mentee_headers = get_auth_headers(client, "mentee@test.com", "password123")
        client.post(
            "/api/match-requests",
            data=json.dumps({"mentor_id": mentor_id, "message": "Test request"}),
            content_type="application/json",
            headers=mentee_headers,
        )

        # Get requests as mentor
        mentor_headers = get_auth_headers(client, "mentor@test.com", "password123")
        response = client.get("/api/match-requests", headers=mentor_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "requests" in data

    def test_accept_request_as_mentor(self, client, app):
        """Test accepting request as mentor"""
        # Create users and a request
        mentor_id = create_test_mentor(app)
        create_test_mentee(app)

        # Create request as mentee
        mentee_headers = get_auth_headers(client, "mentee@test.com", "password123")
        response = client.post(
            "/api/match-requests",
            data=json.dumps({"mentor_id": mentor_id, "message": "Test request"}),
            content_type="application/json",
            headers=mentee_headers,
        )

        # Get the request ID
        response = client.get("/api/match-requests", headers=mentee_headers)
        data = json.loads(response.data)
        request_id = data["requests"][0]["id"]

        # Accept as mentor
        mentor_headers = get_auth_headers(client, "mentor@test.com", "password123")
        response = client.put(
            f"/api/match-requests/{request_id}",
            data=json.dumps({"status": "accepted"}),
            content_type="application/json",
            headers=mentor_headers,
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Match request updated successfully"

    def test_delete_request_as_mentee(self, client, app):
        """Test deleting/canceling request as mentee"""
        # Create users and a request
        mentor_id = create_test_mentor(app)
        create_test_mentee(app)

        # Create request as mentee
        mentee_headers = get_auth_headers(client, "mentee@test.com", "password123")
        response = client.post(
            "/api/match-requests",
            data=json.dumps({"mentor_id": mentor_id, "message": "Test request"}),
            content_type="application/json",
            headers=mentee_headers,
        )

        # Get the request ID
        response = client.get("/api/match-requests", headers=mentee_headers)
        data = json.loads(response.data)
        request_id = data["requests"][0]["id"]

        # Delete as mentee
        response = client.delete(
            f"/api/match-requests/{request_id}", headers=mentee_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Match request deleted successfully"


class TestSecurity:
    """Test security aspects"""

    def test_unauthorized_access_to_protected_routes(self, client):
        """Test that protected routes require authentication"""
        protected_routes = [
            ("/api/profile", "GET"),
            ("/api/mentors", "GET"),
            ("/api/match-requests", "GET"),
            ("/api/match-requests", "POST"),
        ]

        for route, method in protected_routes:
            if method == "GET":
                response = client.get(route)
            elif method == "POST":
                response = client.post(
                    route, data="{}", content_type="application/json"
                )

            assert response.status_code == 401

    def test_sql_injection_protection(self, client, app):
        """Test protection against SQL injection"""
        # Try SQL injection in login
        response = client.post(
            "/api/login",
            data=json.dumps(
                {"email": "'; DROP TABLE users; --", "password": "password"}
            ),
            content_type="application/json",
        )

        # Should not crash the application
        assert response.status_code in [
            400,
            401,
        ]  # Bad request or unauthorized, not 500


if __name__ == "__main__":
    pytest.main([__file__])
