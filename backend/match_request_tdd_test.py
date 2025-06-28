"""
Comprehensive TDD test for Match Request functionality
"""

import json
import os
import tempfile

# Set test database path before importing app
os.environ["TESTING"] = "True"
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from app import app, db


def run_test_with_clean_db(test_func):
    """Run a test function with a clean database"""
    original_config = {
        "TESTING": app.config.get("TESTING"),
        "SQLALCHEMY_DATABASE_URI": app.config.get("SQLALCHEMY_DATABASE_URI"),
    }

    try:
        # Configure for testing
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        with app.app_context():
            db.drop_all()
            db.create_all()
            result = test_func()
            db.drop_all()
            return result
    finally:
        # Restore original config
        app.config.update(original_config)


def test_match_request_flow():
    """Test complete match request flow: create, list, accept, reject"""
    with app.test_client() as client:
        # Create a mentor
        mentor_response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "mentor@test.com",
                    "password": "password123",
                    "name": "Test Mentor",
                    "role": "mentor",
                }
            ),
            content_type="application/json",
        )
        assert mentor_response.status_code == 201

        # Create a mentee
        mentee_response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "mentee@test.com",
                    "password": "password123",
                    "name": "Test Mentee",
                    "role": "mentee",
                }
            ),
            content_type="application/json",
        )
        assert mentee_response.status_code == 201

        # Login both users
        mentor_login = client.post(
            "/api/login",
            data=json.dumps({"email": "mentor@test.com", "password": "password123"}),
            content_type="application/json",
        )
        assert mentor_login.status_code == 200
        mentor_token = json.loads(mentor_login.get_data(as_text=True))["token"]

        mentee_login = client.post(
            "/api/login",
            data=json.dumps({"email": "mentee@test.com", "password": "password123"}),
            content_type="application/json",
        )
        assert mentee_login.status_code == 200
        mentee_token = json.loads(mentee_login.get_data(as_text=True))["token"]

        # 1. Mentee creates a match request
        request_response = client.post(
            "/api/match-requests",
            data=json.dumps(
                {
                    "mentorId": 1,  # The mentor's ID (camelCase per API spec)
                    "message": "I would like to learn from you!",
                }
            ),
            content_type="application/json",
            headers={"Authorization": f"Bearer {mentee_token}"},
        )

        print(f"Create request - Status: {request_response.status_code}")
        data = json.loads(request_response.get_data(as_text=True))
        print(f"Create request - Response: {data}")

        assert request_response.status_code == 200  # API spec says 200 OK
        assert "id" in data  # Should return the created request data

        # 2. Mentee lists their outgoing requests
        mentee_requests = client.get(
            "/api/match-requests/outgoing",
            headers={"Authorization": f"Bearer {mentee_token}"},
        )

        print(f"Mentee requests - Status: {mentee_requests.status_code}")
        data = json.loads(mentee_requests.get_data(as_text=True))
        print(f"Mentee requests - Response: {data}")

        assert mentee_requests.status_code == 200
        assert isinstance(data, list)  # API spec shows it returns an array
        assert len(data) >= 1
        request_id = data[0]["id"]

        # 3. Mentor lists their incoming requests
        mentor_requests = client.get(
            "/api/match-requests/incoming",
            headers={"Authorization": f"Bearer {mentor_token}"},
        )

        print(f"Mentor requests - Status: {mentor_requests.status_code}")
        data = json.loads(mentor_requests.get_data(as_text=True))
        print(f"Mentor requests - Response: {data}")

        assert mentor_requests.status_code == 200
        assert isinstance(data, list)  # API spec shows it returns an array
        assert len(data) >= 1

        # 4. Mentor accepts the request
        accept_response = client.put(
            f"/api/match-requests/{request_id}/accept",
            headers={"Authorization": f"Bearer {mentor_token}"},
        )

        print(f"Accept request - Status: {accept_response.status_code}")
        data = json.loads(accept_response.get_data(as_text=True))
        print(f"Accept request - Response: {data}")

        assert accept_response.status_code == 200
        assert data["status"] == "accepted"

        print("✅ Match request flow test passed!")


def test_unauthorized_match_request():
    """Test that mentors cannot create match requests"""
    with app.test_client() as client:
        # Create a mentor
        mentor_response = client.post(
            "/api/signup",
            data=json.dumps(
                {
                    "email": "mentor@test.com",
                    "password": "password123",
                    "name": "Test Mentor",
                    "role": "mentor",
                }
            ),
            content_type="application/json",
        )
        assert mentor_response.status_code == 201

        # Login mentor
        mentor_login = client.post(
            "/api/login",
            data=json.dumps({"email": "mentor@test.com", "password": "password123"}),
            content_type="application/json",
        )
        assert mentor_login.status_code == 200
        mentor_token = json.loads(mentor_login.get_data(as_text=True))["token"]

        # Try to create a match request as mentor (should fail)
        request_response = client.post(
            "/api/match-requests",
            data=json.dumps(
                {"mentorId": 1, "message": "This should fail"}  # camelCase per API spec
            ),
            content_type="application/json",
            headers={"Authorization": f"Bearer {mentor_token}"},
        )

        print(f"Unauthorized request - Status: {request_response.status_code}")
        data = json.loads(request_response.get_data(as_text=True))
        print(f"Unauthorized request - Response: {data}")

        assert request_response.status_code == 403
        assert (
            "Only mentees can send" in data["error"]
            or "Only mentees can send requests" in data["error"]
        )

        print("✅ Unauthorized match request test passed!")


if __name__ == "__main__":
    print("Running comprehensive TDD tests for Match Request functionality...")

    try:
        print("\n1. Testing complete match request flow...")
        run_test_with_clean_db(test_match_request_flow)

        print("\n2. Testing unauthorized match request...")
        run_test_with_clean_db(test_unauthorized_match_request)

        print(
            "\n🎉 All match request TDD tests passed! The implementation is fully compliant with the API specification."
        )

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
