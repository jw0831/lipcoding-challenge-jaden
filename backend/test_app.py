import pytest
import json
import tempfile
import os
from app import app, db, User, MentorSkill, MatchingRequest
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    """Create a test client"""
    # Create a temporary database file
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def mentor_user(app):
    """Create a test mentor user"""
    with app.app_context():
        user = User(
            email='mentor@test.com',
            password_hash=generate_password_hash('password123'),
            name='Test Mentor',
            role='mentor',
            bio='I am a test mentor'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def mentee_user(app):
    """Create a test mentee user"""
    with app.app_context():
        user = User(
            email='mentee@test.com',
            password_hash=generate_password_hash('password123'),
            name='Test Mentee',
            role='mentee',
            bio='I am a test mentee'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def auth_headers_mentor(client, mentor_user):
    """Get authentication headers for mentor"""
    response = client.post('/api/login', 
                          data=json.dumps({
                              'email': 'mentor@test.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    data = json.loads(response.data)
    token = data['token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def auth_headers_mentee(client, mentee_user):
    """Get authentication headers for mentee"""
    response = client.post('/api/login', 
                          data=json.dumps({
                              'email': 'mentee@test.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    data = json.loads(response.data)
    token = data['token']
    return {'Authorization': f'Bearer {token}'}


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_signup_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/signup',
                              data=json.dumps({
                                  'email': 'newuser@test.com',
                                  'password': 'password123',
                                  'name': 'New User',
                                  'role': 'mentor'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
    
    def test_signup_duplicate_email(self, client, mentor_user):
        """Test signup with duplicate email"""
        response = client.post('/api/signup',
                              data=json.dumps({
                                  'email': 'mentor@test.com',
                                  'password': 'password123',
                                  'name': 'Another User',
                                  'role': 'mentee'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already registered' in data['error']
    
    def test_signup_invalid_role(self, client):
        """Test signup with invalid role"""
        response = client.post('/api/signup',
                              data=json.dumps({
                                  'email': 'newuser@test.com',
                                  'password': 'password123',
                                  'name': 'New User',
                                  'role': 'invalid_role'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_login_success(self, client, mentor_user):
        """Test successful login"""
        response = client.post('/api/login',
                              data=json.dumps({
                                  'email': 'mentor@test.com',
                                  'password': 'password123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
    
    def test_login_invalid_credentials(self, client, mentor_user):
        """Test login with invalid credentials"""
        response = client.post('/api/login',
                              data=json.dumps({
                                  'email': 'mentor@test.com',
                                  'password': 'wrongpassword'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['error']


class TestProfile:
    """Test profile management endpoints"""
    
    def test_get_profile_mentor(self, client, mentor_user, auth_headers_mentor):
        """Test getting mentor profile"""
        response = client.get('/api/me', headers=auth_headers_mentor)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'mentor@test.com'
        assert data['role'] == 'mentor'
        assert 'profile' in data
        assert 'skills' in data['profile']
    
    def test_get_profile_mentee(self, client, mentee_user, auth_headers_mentee):
        """Test getting mentee profile"""
        response = client.get('/api/me', headers=auth_headers_mentee)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'mentee@test.com'
        assert data['role'] == 'mentee'
        assert 'profile' in data
        assert 'skills' not in data['profile']  # Mentees don't have skills
    
    def test_update_profile_mentor(self, client, mentor_user, auth_headers_mentor):
        """Test updating mentor profile"""
        response = client.put('/api/me',
                             data=json.dumps({
                                 'name': 'Updated Mentor',
                                 'bio': 'Updated bio',
                                 'skills': ['Python', 'JavaScript']
                             }),
                             content_type='application/json',
                             headers=auth_headers_mentor)
        
        assert response.status_code == 200
        
        # Verify the update
        response = client.get('/api/me', headers=auth_headers_mentor)
        data = json.loads(response.data)
        assert data['profile']['name'] == 'Updated Mentor'
        assert data['profile']['bio'] == 'Updated bio'
        assert 'Python' in data['profile']['skills']
        assert 'JavaScript' in data['profile']['skills']
    
    def test_get_profile_unauthorized(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/me')
        assert response.status_code == 401


class TestMentorListing:
    """Test mentor listing endpoints"""
    
    def test_get_mentors_as_mentee(self, client, mentor_user, mentee_user, auth_headers_mentee):
        """Test getting mentor list as mentee"""
        # Add skills to mentor
        skill1 = MentorSkill(user_id=mentor_user.id, skill='Python')
        skill2 = MentorSkill(user_id=mentor_user.id, skill='React')
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.commit()
        
        response = client.get('/api/mentors', headers=auth_headers_mentee)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        
        mentor_data = data[0]
        assert mentor_data['id'] == mentor_user.id
        assert mentor_data['profile']['name'] == mentor_user.name
        assert 'Python' in mentor_data['profile']['skills']
        assert 'React' in mentor_data['profile']['skills']
    
    def test_get_mentors_with_skill_filter(self, client, mentor_user, mentee_user, auth_headers_mentee):
        """Test getting mentors with skill filter"""
        # Add skills to mentor
        skill1 = MentorSkill(user_id=mentor_user.id, skill='Python')
        skill2 = MentorSkill(user_id=mentor_user.id, skill='JavaScript')
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.commit()
        
        response = client.get('/api/mentors?skill=Python', headers=auth_headers_mentee)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        
        # All returned mentors should have Python skill
        for mentor in data:
            assert 'Python' in mentor['profile']['skills']


class TestMatchingRequests:
    """Test matching request endpoints"""
    
    def test_create_request_as_mentee(self, client, mentor_user, mentee_user, auth_headers_mentee):
        """Test creating a matching request as mentee"""
        response = client.post('/api/requests',
                              data=json.dumps({
                                  'mentorId': mentor_user.id,
                                  'message': 'I would like mentoring'
                              }),
                              content_type='application/json',
                              headers=auth_headers_mentee)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Request sent successfully'
    
    def test_create_request_as_mentor_fails(self, client, mentor_user, mentee_user, auth_headers_mentor):
        """Test that mentors cannot create requests"""
        response = client.post('/api/requests',
                              data=json.dumps({
                                  'mentorId': mentee_user.id,
                                  'message': 'This should fail'
                              }),
                              content_type='application/json',
                              headers=auth_headers_mentor)
        
        assert response.status_code == 403
    
    def test_get_requests_as_mentee(self, client, mentor_user, mentee_user, auth_headers_mentee):
        """Test getting requests as mentee"""
        # Create a request first
        request = MatchingRequest(
            mentor_id=mentor_user.id,
            mentee_id=mentee_user.id,
            message='Test request',
            status='pending'
        )
        db.session.add(request)
        db.session.commit()
        
        response = client.get('/api/requests', headers=auth_headers_mentee)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        
        request_data = data[0]
        assert request_data['message'] == 'Test request'
        assert request_data['status'] == 'pending'
    
    def test_get_requests_as_mentor(self, client, mentor_user, mentee_user, auth_headers_mentor):
        """Test getting requests as mentor"""
        # Create a request first
        request = MatchingRequest(
            mentor_id=mentor_user.id,
            mentee_id=mentee_user.id,
            message='Test request',
            status='pending'
        )
        db.session.add(request)
        db.session.commit()
        
        response = client.get('/api/requests', headers=auth_headers_mentor)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        
        request_data = data[0]
        assert request_data['message'] == 'Test request'
        assert request_data['status'] == 'pending'
    
    def test_accept_request_as_mentor(self, client, mentor_user, mentee_user, auth_headers_mentor):
        """Test accepting a request as mentor"""
        # Create a request first
        request = MatchingRequest(
            mentor_id=mentor_user.id,
            mentee_id=mentee_user.id,
            message='Test request',
            status='pending'
        )
        db.session.add(request)
        db.session.commit()
        
        response = client.put(f'/api/requests/{request.id}',
                             data=json.dumps({'status': 'accepted'}),
                             content_type='application/json',
                             headers=auth_headers_mentor)
        
        assert response.status_code == 200
        
        # Verify the request was accepted
        updated_request = MatchingRequest.query.get(request.id)
        assert updated_request.status == 'accepted'
    
    def test_delete_request_as_mentee(self, client, mentor_user, mentee_user, auth_headers_mentee):
        """Test deleting a request as mentee"""
        # Create a request first
        request = MatchingRequest(
            mentor_id=mentor_user.id,
            mentee_id=mentee_user.id,
            message='Test request',
            status='pending'
        )
        db.session.add(request)
        db.session.commit()
        request_id = request.id
        
        response = client.delete(f'/api/requests/{request_id}', headers=auth_headers_mentee)
        
        assert response.status_code == 200
        
        # Verify the request was deleted
        deleted_request = MatchingRequest.query.get(request_id)
        assert deleted_request is None


class TestSecurity:
    """Test security features"""
    
    def test_unauthorized_access_to_protected_routes(self, client):
        """Test that protected routes require authentication"""
        protected_routes = [
            ('/api/me', 'GET'),
            ('/api/me', 'PUT'),
            ('/api/mentors', 'GET'),
            ('/api/requests', 'GET'),
            ('/api/requests', 'POST')
        ]
        
        for route, method in protected_routes:
            if method == 'GET':
                response = client.get(route)
            elif method == 'PUT':
                response = client.put(route, data=json.dumps({}), content_type='application/json')
            elif method == 'POST':
                response = client.post(route, data=json.dumps({}), content_type='application/json')
            
            assert response.status_code == 401
    
    def test_sql_injection_protection(self, client):
        """Test protection against SQL injection"""
        malicious_data = {
            'email': "test@test.com'; DROP TABLE users; --",
            'password': 'password123',
            'name': 'Test User',
            'role': 'mentor'
        }
        
        response = client.post('/api/signup',
                              data=json.dumps(malicious_data),
                              content_type='application/json')
        
        # Should either create user safely or return validation error
        # but should not cause database corruption
        assert response.status_code in [201, 400]
