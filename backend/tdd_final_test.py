"""
Simple TDD test suite for the Mentor-Mentee Matching Application API
Tests core functionality according to the API specification
"""
import json
import os
import tempfile
import sys

# Set test database path before importing app
test_db_path = ':memory:'  # Use in-memory database for tests
os.environ['TESTING'] = 'True'
os.environ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{test_db_path}'

from app import app, db


def run_test_with_clean_db(test_func):
    """Run a test function with a clean database"""
    original_config = {
        'TESTING': app.config.get('TESTING'),
        'SQLALCHEMY_DATABASE_URI': app.config.get('SQLALCHEMY_DATABASE_URI')
    }
    
    try:
        # Configure for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.drop_all()
            db.create_all()
            result = test_func()
            db.drop_all()
            return result
    finally:
        # Restore original config
        app.config.update(original_config)


def test_signup_new_user():
    """Test successful user registration"""
    with app.test_client() as client:
        response = client.post('/api/signup',
                              data=json.dumps({
                                  'email': 'newuser@test.com',
                                  'password': 'password123',
                                  'name': 'New User',
                                  'role': 'mentor'
                              }),
                              content_type='application/json')
        
        print(f"Signup test - Status: {response.status_code}")
        data = json.loads(response.get_data(as_text=True))
        print(f"Signup test - Response: {data}")
        
        assert response.status_code == 201
        assert data['message'] == 'User created successfully'
        # Note: According to API spec, signup doesn't return token


def test_login_existing_user():
    """Test successful login"""
    with app.test_client() as client:
        # First, create a user
        signup_response = client.post('/api/signup',
                                    data=json.dumps({
                                        'email': 'testuser@test.com',
                                        'password': 'password123',
                                        'name': 'Test User',
                                        'role': 'mentee'
                                    }),
                                    content_type='application/json')
        
        assert signup_response.status_code == 201
        
        # Now try to login
        login_response = client.post('/api/login',
                                   data=json.dumps({
                                       'email': 'testuser@test.com',
                                       'password': 'password123'
                                   }),
                                   content_type='application/json')
        
        print(f"Login test - Status: {login_response.status_code}")
        data = json.loads(login_response.get_data(as_text=True))
        print(f"Login test - Response: {data}")
        
        assert login_response.status_code == 200
        assert 'token' in data


def test_profile_access():
    """Test profile access with authentication"""
    with app.test_client() as client:
        # Create and login a user
        signup_response = client.post('/api/signup',
                                    data=json.dumps({
                                        'email': 'profile@test.com',
                                        'password': 'password123',
                                        'name': 'Profile User',
                                        'role': 'mentor'
                                    }),
                                    content_type='application/json')
        
        assert signup_response.status_code == 201
        
        # Login to get token
        login_response = client.post('/api/login',
                                   data=json.dumps({
                                       'email': 'profile@test.com',
                                       'password': 'password123'
                                   }),
                                   content_type='application/json')
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.get_data(as_text=True))
        token = login_data['token']
        
        # Test profile access
        profile_response = client.get('/api/profile',
                                    headers={'Authorization': f'Bearer {token}'})
        
        print(f"Profile test - Status: {profile_response.status_code}")
        data = json.loads(profile_response.get_data(as_text=True))
        print(f"Profile test - Response: {data}")
        
        assert profile_response.status_code == 200
        assert data['email'] == 'profile@test.com'
        assert data['role'] == 'mentor'
        assert data['name'] == 'Profile User'


def test_unauthorized_access():
    """Test that protected routes require authentication"""
    with app.test_client() as client:
        # Try to access protected route without token
        response = client.get('/api/profile')
        
        print(f"Unauthorized test - Status: {response.status_code}")
        print(f"Unauthorized test - Response: {response.get_data(as_text=True)}")
        
        assert response.status_code == 401


def test_mentors_listing():
    """Test mentor listing for mentees"""
    with app.test_client() as client:
        # Create a mentor
        mentor_response = client.post('/api/signup',
                                    data=json.dumps({
                                        'email': 'mentor@test.com',
                                        'password': 'password123',
                                        'name': 'Test Mentor',
                                        'role': 'mentor'
                                    }),
                                    content_type='application/json')
        assert mentor_response.status_code == 201
        
        # Create a mentee
        mentee_response = client.post('/api/signup',
                                    data=json.dumps({
                                        'email': 'mentee@test.com',
                                        'password': 'password123',
                                        'name': 'Test Mentee',
                                        'role': 'mentee'
                                    }),
                                    content_type='application/json')
        assert mentee_response.status_code == 201
        
        # Login mentee to get token
        login_response = client.post('/api/login',
                                   data=json.dumps({
                                       'email': 'mentee@test.com',
                                       'password': 'password123'
                                   }),
                                   content_type='application/json')
        assert login_response.status_code == 200
        login_data = json.loads(login_response.get_data(as_text=True))
        mentee_token = login_data['token']
        
        # Test mentors listing as mentee
        mentors_response = client.get('/api/mentors',
                                    headers={'Authorization': f'Bearer {mentee_token}'})
        
        print(f"Mentors listing test - Status: {mentors_response.status_code}")
        data = json.loads(mentors_response.get_data(as_text=True))
        print(f"Mentors listing test - Response: {data}")
        
        assert mentors_response.status_code == 200
        # According to API spec, mentors endpoint returns an array directly
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['role'] == 'mentor'
        assert 'profile' in data[0]


if __name__ == '__main__':
    print("Running TDD tests for Mentor-Mentee Matching API...")
    
    try:
        print("\n1. Testing user signup...")
        run_test_with_clean_db(test_signup_new_user)
        print("✅ Signup test passed")
        
        print("\n2. Testing user login...")
        run_test_with_clean_db(test_login_existing_user)
        print("✅ Login test passed")
        
        print("\n3. Testing profile access...")
        run_test_with_clean_db(test_profile_access)
        print("✅ Profile access test passed")
        
        print("\n4. Testing unauthorized access...")
        run_test_with_clean_db(test_unauthorized_access)
        print("✅ Unauthorized access test passed")
        
        print("\n5. Testing mentors listing...")
        run_test_with_clean_db(test_mentors_listing)
        print("✅ Mentors listing test passed")
        
        print("\n🎉 All TDD tests passed! The API implementation meets the specification requirements.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
