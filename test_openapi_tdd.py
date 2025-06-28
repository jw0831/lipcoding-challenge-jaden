#!/usr/bin/env python3
"""
TDD Test Suite for OpenAPI Integration
This test suite follows Test-Driven Development principles to ensure
the OpenAPI YAML integration is working correctly with the Flask application.
"""

import pytest
import requests
import json
import yaml
import os
import sys
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:8080"
API_BASE_URL = f"{BASE_URL}/api"

class TestOpenAPIIntegration:
    """Test class for OpenAPI integration following TDD principles"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.base_url = BASE_URL
        self.api_base_url = API_BASE_URL
        
    def test_openapi_yaml_file_exists(self):
        """TDD Test 1: Verify OpenAPI YAML file exists in project root"""
        project_root = Path(__file__).parent
        openapi_file = project_root / "openapi.yaml"
        
        assert openapi_file.exists(), "OpenAPI YAML file should exist in project root"
        assert openapi_file.is_file(), "OpenAPI YAML should be a file, not directory"
        
        # Verify file is not empty
        assert openapi_file.stat().st_size > 0, "OpenAPI YAML file should not be empty"
        
    def test_openapi_yaml_is_valid_yaml(self):
        """TDD Test 2: Verify OpenAPI YAML file contains valid YAML"""
        project_root = Path(__file__).parent
        openapi_file = project_root / "openapi.yaml"
        
        with open(openapi_file, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Should be able to parse as valid YAML
        try:
            parsed_yaml = yaml.safe_load(content)
            assert parsed_yaml is not None, "YAML content should not be None"
            assert isinstance(parsed_yaml, dict), "YAML should parse to a dictionary"
        except yaml.YAMLError as e:
            pytest.fail(f"OpenAPI YAML file contains invalid YAML: {e}")
            
    def test_openapi_yaml_has_required_structure(self):
        """TDD Test 3: Verify OpenAPI YAML has required OpenAPI 3.0 structure"""
        project_root = Path(__file__).parent
        openapi_file = project_root / "openapi.yaml"
        
        with open(openapi_file, 'r', encoding='utf-8') as file:
            spec = yaml.safe_load(file)
            
        # Test required OpenAPI 3.0 fields
        assert 'openapi' in spec, "OpenAPI spec must have 'openapi' field"
        assert spec['openapi'].startswith('3.0'), "Should be OpenAPI 3.0+ specification"
        
        assert 'info' in spec, "OpenAPI spec must have 'info' section"
        assert 'title' in spec['info'], "Info section must have 'title'"
        assert 'version' in spec['info'], "Info section must have 'version'"
        
        assert 'paths' in spec, "OpenAPI spec must have 'paths' section"
        assert isinstance(spec['paths'], dict), "Paths should be a dictionary"
        
    def test_flask_server_is_running(self):
        """TDD Test 4: Verify Flask server is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            # Should either get a successful response or a redirect (3xx)
            assert response.status_code in [200, 301, 302, 308], \
                f"Flask server should be running (got status {response.status_code})"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Flask server is not accessible: {e}")
            
    def test_openapi_json_endpoint_exists(self):
        """TDD Test 5: Verify /openapi.json endpoint exists and returns JSON"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        
        assert response.status_code == 200, \
            f"OpenAPI JSON endpoint should return 200 (got {response.status_code})"
        
        content_type = response.headers.get('content-type', '').lower()
        assert 'application/json' in content_type, \
            f"OpenAPI JSON should return JSON content-type (got {content_type})"
            
    def test_openapi_json_response_is_valid_json(self):
        """TDD Test 6: Verify /openapi.json returns valid JSON"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        
        try:
            json_data = response.json()
            assert isinstance(json_data, dict), "OpenAPI JSON should be a dictionary"
        except json.JSONDecodeError as e:
            pytest.fail(f"OpenAPI JSON endpoint returns invalid JSON: {e}")
            
    def test_openapi_json_has_correct_structure(self):
        """TDD Test 7: Verify /openapi.json has correct OpenAPI structure"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        spec = response.json()
        
        # Test OpenAPI structure
        assert 'openapi' in spec, "JSON spec must have 'openapi' field"
        assert 'info' in spec, "JSON spec must have 'info' section"
        assert 'paths' in spec, "JSON spec must have 'paths' section"
        
        # Test that it matches our YAML file structure
        assert spec['openapi'].startswith('3.0'), "Should be OpenAPI 3.0+ specification"
        assert spec['info']['title'] == "Mentor-Mentee Matching API", "Title should match YAML"
        
    def test_openapi_yaml_endpoint_exists(self):
        """TDD Test 8: Verify /openapi.yaml endpoint exists and returns YAML"""
        response = requests.get(f"{self.base_url}/openapi.yaml", timeout=5)
        
        assert response.status_code == 200, \
            f"OpenAPI YAML endpoint should return 200 (got {response.status_code})"
            
        content_type = response.headers.get('content-type', '').lower()
        assert 'yaml' in content_type or 'text/plain' in content_type, \
            f"OpenAPI YAML should return YAML content-type (got {content_type})"
            
    def test_openapi_yaml_endpoint_returns_valid_yaml(self):
        """TDD Test 9: Verify /openapi.yaml returns valid YAML content"""
        response = requests.get(f"{self.base_url}/openapi.yaml", timeout=5)
        
        try:
            yaml_data = yaml.safe_load(response.text)
            assert isinstance(yaml_data, dict), "OpenAPI YAML should parse to a dictionary"
        except yaml.YAMLError as e:
            pytest.fail(f"OpenAPI YAML endpoint returns invalid YAML: {e}")
            
    def test_swagger_ui_endpoint_exists(self):
        """TDD Test 10: Verify Swagger UI endpoints exist"""
        endpoints = ["/api-docs", "/swagger-ui"]
        
        for endpoint in endpoints:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
            assert response.status_code == 200, \
                f"Swagger UI endpoint {endpoint} should return 200 (got {response.status_code})"
                
            content_type = response.headers.get('content-type', '').lower()
            assert 'text/html' in content_type, \
                f"Swagger UI should return HTML content-type (got {content_type})"
                
    def test_swagger_ui_contains_required_elements(self):
        """TDD Test 11: Verify Swagger UI HTML contains required elements"""
        response = requests.get(f"{self.base_url}/api-docs", timeout=5)
        html_content = response.text.lower()
        
        # Check for essential Swagger UI elements
        assert 'swagger' in html_content, "Swagger UI should contain 'swagger' reference"
        assert 'swagger-ui' in html_content, "Should contain swagger-ui div or script"
        assert 'openapi.json' in html_content, "Should reference openapi.json for spec loading"
        
    def test_yaml_and_json_specs_are_equivalent(self):
        """TDD Test 12: Verify YAML and JSON specs contain equivalent data"""
        # Get both specs
        json_response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        yaml_response = requests.get(f"{self.base_url}/openapi.yaml", timeout=5)
        
        json_spec = json_response.json()
        yaml_spec = yaml.safe_load(yaml_response.text)
        
        # Compare key fields
        assert json_spec['openapi'] == yaml_spec['openapi'], \
            "OpenAPI version should match between JSON and YAML"
        assert json_spec['info']['title'] == yaml_spec['info']['title'], \
            "API title should match between JSON and YAML"
        assert json_spec['info']['version'] == yaml_spec['info']['version'], \
            "API version should match between JSON and YAML"
        assert len(json_spec['paths']) == len(yaml_spec['paths']), \
            "Number of paths should match between JSON and YAML"
            
    def test_documented_endpoints_exist_in_spec(self):
        """TDD Test 13: Verify key API endpoints are documented in spec"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        spec = response.json()
        paths = spec.get('paths', {})
        
        # Test that key endpoints are documented
        expected_endpoints = [
            '/signup',
            '/login', 
            '/me',
            '/mentors',
            '/match-requests',
            '/profile'
        ]
        
        for endpoint in expected_endpoints:
            assert endpoint in paths, f"Endpoint {endpoint} should be documented in OpenAPI spec"
            
    def test_api_endpoints_match_documentation(self):
        """TDD Test 14: Verify actual API endpoints match OpenAPI documentation"""
        response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
        spec = response.json()
        paths = spec.get('paths', {})
        
        # Test a few key endpoints to ensure they're actually implemented
        test_cases = [
            ('/signup', 'post', [400, 201]),  # Should accept POST, reject without data
            ('/login', 'post', [400, 401]),   # Should accept POST, reject without data
            ('/me', 'get', [401]),            # Should require authentication
        ]
        
        for path, method, expected_statuses in test_cases:
            full_url = f"{self.api_base_url}{path}"
            
            # Verify endpoint is documented
            assert path in paths, f"Path {path} should be in OpenAPI spec"
            assert method in paths[path], f"Method {method} should be documented for {path}"
            
            # Test actual endpoint
            try:
                if method.lower() == 'get':
                    api_response = requests.get(full_url, timeout=5)
                elif method.lower() == 'post':
                    api_response = requests.post(full_url, json={}, timeout=5)
                else:
                    continue
                    
                assert api_response.status_code in expected_statuses, \
                    f"Endpoint {method.upper()} {path} returned unexpected status {api_response.status_code}"
                    
            except requests.exceptions.RequestException:
                pytest.fail(f"Endpoint {method.upper()} {path} is not accessible")
                
    def test_cors_headers_are_present(self):
        """TDD Test 15: Verify CORS headers are properly configured"""
        # Test CORS on OpenAPI endpoints
        endpoints = ['/openapi.json', '/api/me']
        
        for endpoint in endpoints:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
            
            # Check for CORS headers (at least some should be present)
            cors_headers = [
                'access-control-allow-origin',
                'access-control-allow-methods', 
                'access-control-allow-headers'
            ]
            
            headers_lower = {k.lower(): v for k, v in response.headers.items()}
            has_cors = any(header in headers_lower for header in cors_headers)
            
            # For API endpoints, CORS should be configured
            if '/api/' in endpoint:
                assert has_cors, f"API endpoint {endpoint} should have CORS headers"


def test_openapi_integration_summary():
    """TDD Test 16: Integration summary test"""
    print("\n" + "="*60)
    print("🧪 OpenAPI Integration TDD Test Summary")
    print("="*60)
    
    # Test basic connectivity
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        json_spec = response.json()
        
        print(f"✅ OpenAPI Version: {json_spec.get('openapi', 'Unknown')}")
        print(f"✅ API Title: {json_spec.get('info', {}).get('title', 'Unknown')}")
        print(f"✅ API Version: {json_spec.get('info', {}).get('version', 'Unknown')}")
        print(f"✅ Documented Endpoints: {len(json_spec.get('paths', {}))}")
        
        # List documented endpoints
        paths = json_spec.get('paths', {})
        if paths:
            print(f"\n📋 Documented API Endpoints:")
            for path, methods in paths.items():
                for method in methods:
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        print(f"   {method.upper()} {path}")
                        
        print(f"\n🌐 Access Points:")
        print(f"   📚 API Documentation: {BASE_URL}/api-docs")
        print(f"   📄 OpenAPI JSON: {BASE_URL}/openapi.json")  
        print(f"   📄 OpenAPI YAML: {BASE_URL}/openapi.yaml")
        
    except Exception as e:
        print(f"❌ Error in integration summary: {e}")
        
    print("="*60)


if __name__ == "__main__":
    # Run the integration summary first
    test_openapi_integration_summary()
    
    # Run all tests with pytest
    print("\n🚀 Running TDD Test Suite...")
    pytest.main([__file__, "-v", "--tb=short"])
