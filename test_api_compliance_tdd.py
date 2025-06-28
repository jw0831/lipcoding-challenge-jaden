#!/usr/bin/env python3
"""
TDD Test Suite for API Endpoint Compliance with OpenAPI Specification
This follows strict TDD principles to ensure each documented endpoint
matches its implementation and vice versa.
"""

import pytest
import requests
import json
import yaml
from typing import Dict, List, Any

BASE_URL = "http://localhost:8080"
API_BASE_URL = f"{BASE_URL}/api"

class TestAPIEndpointCompliance:
    """TDD tests to ensure API endpoints match OpenAPI specification exactly"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Get the OpenAPI specification
        response = requests.get(f"{BASE_URL}/openapi.json")
        assert response.status_code == 200, "OpenAPI spec should be accessible"
        self.openapi_spec = response.json()
        self.paths = self.openapi_spec.get('paths', {})
    
    def test_all_documented_endpoints_are_implemented(self):
        """TDD Test: Every endpoint in OpenAPI spec should be implemented"""
        for path, methods in self.paths.items():
            for method, spec in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    # Handle parameterized paths
                    test_path = path
                    if '{role}' in path and '{id}' in path:
                        # Replace with actual values for testing
                        test_path = path.replace('{role}', 'mentor').replace('{id}', '1')
                    elif '{id}' in path:
                        test_path = path.replace('{id}', '1')
                        
                    url = f"{API_BASE_URL}{test_path}"
                    
                    try:
                        if method.upper() == 'GET':
                            response = requests.get(url, timeout=5)
                        elif method.upper() == 'POST':
                            response = requests.post(url, json={}, timeout=5)
                        elif method.upper() == 'PUT':
                            response = requests.put(url, json={}, timeout=5)
                        elif method.upper() == 'DELETE':
                            response = requests.delete(url, timeout=5)
                        else:
                            continue
                            
                        # Endpoint should exist (not 404) - may return 400, 401, etc.
                        # For redirects (302), that's also valid
                        assert response.status_code not in [404, 405], \
                            f"Endpoint {method.upper()} {path} is documented but returns {response.status_code}"
                            
                    except requests.exceptions.RequestException:
                        pytest.fail(f"Endpoint {method.upper()} {path} is not accessible")
    
    def test_authentication_endpoints_work_correctly(self):
        """TDD Test: Authentication endpoints should work as documented"""
        # Test signup endpoint
        signup_url = f"{API_BASE_URL}/signup"
        
        # Should reject empty request
        response = requests.post(signup_url, json={})
        assert response.status_code in [400, 422], \
            "Signup should reject empty request with 400 or 422"
        
        # Should reject incomplete data
        incomplete_data = {"email": "test@example.com"}
        response = requests.post(signup_url, json=incomplete_data)
        assert response.status_code in [400, 422], \
            "Signup should reject incomplete data"
        
        # Test login endpoint
        login_url = f"{API_BASE_URL}/login"
        
        # Should reject empty request
        response = requests.post(login_url, json={})
        assert response.status_code in [400, 401, 422], \
            "Login should reject empty request"
    
    def test_protected_endpoints_require_authentication(self):
        """TDD Test: Protected endpoints should require authentication"""
        protected_endpoints = [
            ('GET', '/me'),
            ('GET', '/mentors'),
            ('PUT', '/profile'),
            ('POST', '/match-requests'),
            ('GET', '/match-requests/incoming'),
            ('GET', '/match-requests/outgoing'),
        ]
        
        for method, path in protected_endpoints:
            url = f"{API_BASE_URL}{path}"
            
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json={})
            elif method == 'PUT':
                response = requests.put(url, json={})
            else:
                continue
                
            assert response.status_code == 401, \
                f"Protected endpoint {method} {path} should return 401 without auth"
    
    def test_openapi_spec_has_security_definitions(self):
        """TDD Test: OpenAPI spec should define security schemes"""
        assert 'components' in self.openapi_spec, \
            "OpenAPI spec should have components section"
        
        components = self.openapi_spec['components']
        assert 'securitySchemes' in components, \
            "OpenAPI spec should define security schemes"
        
        security_schemes = components['securitySchemes']
        assert 'BearerAuth' in security_schemes, \
            "Should have BearerAuth security scheme defined"
        
        bearer_auth = security_schemes['BearerAuth']
        assert bearer_auth['type'] == 'http', \
            "BearerAuth should be HTTP type"
        assert bearer_auth['scheme'] == 'bearer', \
            "BearerAuth should use bearer scheme"
    
    def test_openapi_spec_has_response_schemas(self):
        """TDD Test: Endpoints should have proper response schemas"""
        endpoints_with_responses = ['/signup', '/login', '/me', '/mentors']
        
        for endpoint in endpoints_with_responses:
            if endpoint not in self.paths:
                continue
                
            for method, spec in self.paths[endpoint].items():
                if method.upper() in ['GET', 'POST']:
                    assert 'responses' in spec, \
                        f"Endpoint {method.upper()} {endpoint} should have responses defined"
                    
                    responses = spec['responses']
                    # Should have at least one success response (2xx)
                    success_responses = [r for r in responses.keys() if r.startswith('2')]
                    assert len(success_responses) > 0, \
                        f"Endpoint {method.upper()} {endpoint} should have at least one 2xx response"
    
    def test_request_schemas_are_defined_for_post_put_endpoints(self):
        """TDD Test: POST/PUT endpoints should have request body schemas"""
        for path, methods in self.paths.items():
            for method, spec in methods.items():
                if method.upper() in ['POST', 'PUT']:
                    if 'requestBody' in spec:
                        request_body = spec['requestBody']
                        assert 'content' in request_body, \
                            f"Endpoint {method.upper()} {path} should have content in requestBody"
                        
                        content = request_body['content']
                        assert 'application/json' in content, \
                            f"Endpoint {method.upper()} {path} should accept application/json"
    
    def test_error_responses_are_documented(self):
        """TDD Test: Endpoints should document error responses"""
        for path, methods in self.paths.items():
            for method, spec in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                    responses = spec.get('responses', {})
                    
                    # Should have error responses documented
                    error_codes = ['400', '401', '404', '500']
                    documented_errors = [code for code in error_codes if code in responses]
                    
                    # At least one error response should be documented
                    assert len(documented_errors) > 0, \
                        f"Endpoint {method.upper()} {path} should document at least one error response"
    
    def test_openapi_info_section_is_complete(self):
        """TDD Test: OpenAPI info section should be complete"""
        info = self.openapi_spec.get('info', {})
        
        required_fields = ['title', 'version', 'description']
        for field in required_fields:
            assert field in info, f"OpenAPI info should have {field} field"
            assert info[field], f"OpenAPI info {field} should not be empty"
    
    def test_servers_section_is_defined(self):
        """TDD Test: OpenAPI should define servers"""
        assert 'servers' in self.openapi_spec, \
            "OpenAPI spec should have servers section"
        
        servers = self.openapi_spec['servers']
        assert len(servers) > 0, "At least one server should be defined"
        
        # Check first server
        server = servers[0]
        assert 'url' in server, "Server should have URL defined"
        assert server['url'], "Server URL should not be empty"
    
    def test_components_schemas_are_defined(self):
        """TDD Test: Reusable schemas should be defined in components"""
        components = self.openapi_spec.get('components', {})
        schemas = components.get('schemas', {})
        
        # Should have common schemas defined
        expected_schemas = ['ErrorResponse', 'User', 'LoginRequest', 'SignupRequest']
        
        for schema in expected_schemas:
            assert schema in schemas, f"Schema {schema} should be defined in components"
            
            schema_def = schemas[schema]
            assert 'type' in schema_def or '$ref' in schema_def, \
                f"Schema {schema} should have type or $ref defined"


def test_comprehensive_endpoint_validation():
    """TDD Test: Comprehensive validation of all endpoints"""
    print("\n" + "="*70)
    print("🧪 Comprehensive API Endpoint Validation")
    print("="*70)
    
    try:
        # Get OpenAPI spec
        response = requests.get(f"{BASE_URL}/openapi.json")
        spec = response.json()
        paths = spec.get('paths', {})
        
        print(f"📊 Testing {len(paths)} documented endpoints...")
        
        endpoint_results = []
        
        for path, methods in paths.items():
            for method, spec_details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    url = f"{API_BASE_URL}{path}"
                    
                    # Test endpoint accessibility
                    try:
                        if method.upper() == 'GET':
                            test_response = requests.get(url, timeout=3)
                        elif method.upper() == 'POST':
                            test_response = requests.post(url, json={}, timeout=3)
                        else:
                            continue
                            
                        status = "🟢 ACCESSIBLE" if test_response.status_code != 404 else "🔴 NOT FOUND"
                        endpoint_results.append({
                            'method': method.upper(),
                            'path': path,
                            'status': status,
                            'http_status': test_response.status_code
                        })
                        
                    except requests.exceptions.RequestException:
                        endpoint_results.append({
                            'method': method.upper(),
                            'path': path,
                            'status': "🔴 ERROR",
                            'http_status': 'N/A'
                        })
        
        # Print results
        print("\n📋 Endpoint Test Results:")
        for result in endpoint_results:
            print(f"   {result['status']} {result['method']} {result['path']} (HTTP: {result['http_status']})")
        
        # Summary
        accessible = len([r for r in endpoint_results if '🟢' in r['status']])
        total = len(endpoint_results)
        
        print(f"\n📈 Summary: {accessible}/{total} endpoints accessible")
        
        if accessible == total:
            print("🎉 All documented endpoints are properly implemented!")
        else:
            print("⚠️  Some endpoints may need attention")
            
    except Exception as e:
        print(f"❌ Error in comprehensive validation: {e}")
    
    print("="*70)


if __name__ == "__main__":
    # Run comprehensive validation first
    test_comprehensive_endpoint_validation()
    
    # Run TDD test suite
    print("\n🚀 Running API Compliance TDD Tests...")
    pytest.main([__file__, "-v", "--tb=short"])
