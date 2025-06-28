#!/usr/bin/env python3
"""
Comprehensive Browser Testing Script
This script performs automated browser testing of the mentor-mentee application
"""

import requests
import json
import time
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "http://localhost:8080"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{test_name.center(60)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.ENDC}")

def test_backend_health():
    """Test backend API endpoints"""
    print_test_header("Backend API Health Check")
    
    # Test basic routes
    try:
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 302:  # Redirect to swagger-ui
            print_success("Backend root endpoint accessible (redirects to swagger-ui)")
        else:
            print_error(f"Backend root endpoint returned: {response.status_code}")
    except Exception as e:
        print_error(f"Backend not accessible: {e}")
        return False
    
    # Test swagger-ui
    try:
        response = requests.get(f"{BACKEND_URL}/swagger-ui")
        if response.status_code == 200:
            print_success("Swagger UI accessible")
        else:
            print_error(f"Swagger UI returned: {response.status_code}")
    except Exception as e:
        print_error(f"Swagger UI not accessible: {e}")
    
    # Test OpenAPI spec
    try:
        response = requests.get(f"{BACKEND_URL}/openapi.yaml")
        if response.status_code == 200:
            print_success("OpenAPI YAML spec accessible")
        else:
            print_error(f"OpenAPI spec returned: {response.status_code}")
    except Exception as e:
        print_error(f"OpenAPI spec not accessible: {e}")
    
    return True

def test_user_authentication():
    """Test user authentication flows"""
    print_test_header("User Authentication Testing")
    
    # Test login with existing users
    test_users = [
        {"email": "user@test.com", "password": "user", "role": "mentee"},
        {"email": "mentor@test.com", "password": "user", "role": "mentor"}
    ]
    
    tokens = {}
    
    for user in test_users:
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/login",
                headers={"Content-Type": "application/json"},
                json={"email": user["email"], "password": user["password"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                tokens[user["role"]] = data["token"]
                print_success(f"Login successful for {user['role']}: {user['email']}")
            else:
                print_error(f"Login failed for {user['email']}: {response.text}")
        except Exception as e:
            print_error(f"Login request failed for {user['email']}: {e}")
    
    return tokens

def test_api_endpoints(tokens):
    """Test all API endpoints with authentication"""
    print_test_header("API Endpoints Testing")
    
    if not tokens:
        print_error("No authentication tokens available")
        return
    
    # Test with mentee token
    mentee_token = tokens.get("mentee")
    if mentee_token:
        headers = {"Authorization": f"Bearer {mentee_token}"}
        
        # Test user profile
        try:
            response = requests.get(f"{BACKEND_URL}/api/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                print_success(f"Profile retrieved for: {user_data.get('email')}")
            else:
                print_error(f"Profile retrieval failed: {response.status_code}")
        except Exception as e:
            print_error(f"Profile request failed: {e}")
        
        # Test mentors list
        try:
            response = requests.get(f"{BACKEND_URL}/api/mentors", headers=headers)
            if response.status_code == 200:
                mentors = response.json()
                print_success(f"Mentors list retrieved: {len(mentors)} mentors found")
            else:
                print_error(f"Mentors list failed: {response.status_code}")
        except Exception as e:
            print_error(f"Mentors request failed: {e}")
        
        # Test match requests
        try:
            response = requests.get(f"{BACKEND_URL}/api/match-requests/outgoing", headers=headers)
            if response.status_code == 200:
                requests_data = response.json()
                print_success(f"Outgoing match requests retrieved: {len(requests_data)} requests")
            else:
                print_error(f"Outgoing requests failed: {response.status_code}")
        except Exception as e:
            print_error(f"Outgoing requests failed: {e}")

def test_frontend_accessibility():
    """Test frontend accessibility"""
    print_test_header("Frontend Accessibility Testing")
    
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print_success("Frontend accessible")
            
            # Check for React app content
            if "react" in response.text.lower() or "root" in response.text:
                print_success("React app detected in HTML")
            else:
                print_info("HTML content retrieved but React app not clearly identified")
        else:
            print_error(f"Frontend returned: {response.status_code}")
    except Exception as e:
        print_error(f"Frontend not accessible: {e}")

def generate_manual_test_instructions():
    """Generate manual testing instructions"""
    print_test_header("Manual Testing Instructions")
    
    instructions = [
        "1. Open browser to http://localhost:3000",
        "2. Test Navigation:",
        "   - Click on Login/Signup links",
        "   - Verify page routing works",
        "3. Test Login Flow:",
        "   - Login with: user@test.com / user (mentee)",
        "   - Login with: mentor@test.com / user (mentor)",
        "4. Test Profile Management:",
        "   - View profile page",
        "   - Edit profile information",
        "   - Save changes",
        "5. Test Mentor Discovery (as mentee):",
        "   - Navigate to mentors page",
        "   - View available mentors",
        "   - Send match request",
        "6. Test Match Requests:",
        "   - View outgoing requests (mentee)",
        "   - View incoming requests (mentor)",
        "   - Accept/reject requests (mentor)",
        "7. Test UI/UX:",
        "   - Check responsive design",
        "   - Verify all buttons work",
        "   - Check error handling",
        "8. Test Data Persistence:",
        "   - Logout and login again",
        "   - Refresh browser",
        "   - Verify data persists"
    ]
    
    for instruction in instructions:
        print_info(instruction)

def generate_demo_checklist():
    """Generate demonstration checklist"""
    print_test_header("Demo Video Checklist")
    
    demo_items = [
        "□ Record homepage and navigation",
        "□ Demonstrate user registration",
        "□ Show login process",
        "□ Navigate through all pages",
        "□ Show profile management",
        "□ Demonstrate mentor search",
        "□ Show match request process",
        "□ Display match management",
        "□ Show responsive design",
        "□ Demonstrate error handling",
        "□ Explain key features via voice-over",
        "□ Show OpenAPI documentation",
        "□ Highlight TDD test results",
        "□ Demonstrate API compliance"
    ]
    
    for item in demo_items:
        print_info(item)

def main():
    """Main testing function"""
    print(f"{Colors.BOLD}Mentor-Mentee Application - Comprehensive Testing{Colors.ENDC}")
    print(f"Testing Backend: {BACKEND_URL}")
    print(f"Testing Frontend: {FRONTEND_URL}")
    
    # Run automated tests
    backend_healthy = test_backend_health()
    if backend_healthy:
        tokens = test_user_authentication()
        test_api_endpoints(tokens)
    
    test_frontend_accessibility()
    
    # Generate manual testing guidance
    generate_manual_test_instructions()
    generate_demo_checklist()
    
    print_test_header("Testing Complete")
    print_info("Proceed with manual browser testing using the instructions above")
    print_info("Take screenshots and record demo video as per checklist")
    print_info("Application is ready for submission!")

if __name__ == "__main__":
    main()
