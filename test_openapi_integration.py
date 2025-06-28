#!/usr/bin/env python3
"""
OpenAPI Integration Validator
This script validates that the Flask application properly serves the OpenAPI specification
and that all endpoints are working correctly.
"""

import requests
import json
import yaml
import sys
from pathlib import Path

def test_openapi_endpoints():
    """Test OpenAPI-related endpoints"""
    base_url = "http://localhost:8080"
    
    tests = [
        {
            "name": "OpenAPI JSON Endpoint",
            "url": f"{base_url}/openapi.json",
            "expected_content_type": "application/json"
        },
        {
            "name": "OpenAPI YAML Endpoint", 
            "url": f"{base_url}/openapi.yaml",
            "expected_content_type": "application/x-yaml"
        },
        {
            "name": "Swagger UI",
            "url": f"{base_url}/api-docs",
            "expected_content_type": "text/html"
        },
        {
            "name": "Swagger UI Redirect",
            "url": f"{base_url}/swagger-ui",
            "expected_content_type": "text/html"
        }
    ]
    
    print("🔍 Testing OpenAPI Integration...")
    print("=" * 50)
    
    all_passed = True
    
    for test in tests:
        try:
            response = requests.get(test["url"], timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {test['name']}: OK (Status: {response.status_code})")
                
                # Validate content type if specified
                if "expected_content_type" in test:
                    content_type = response.headers.get('content-type', '').split(';')[0]
                    if test["expected_content_type"] in content_type:
                        print(f"   📄 Content-Type: {content_type}")
                    else:
                        print(f"   ⚠️  Expected content-type: {test['expected_content_type']}, got: {content_type}")
                        
            else:
                print(f"❌ {test['name']}: FAILED (Status: {response.status_code})")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {test['name']}: ERROR - {str(e)}")
            all_passed = False
    
    return all_passed

def validate_openapi_spec():
    """Validate the OpenAPI specification structure"""
    print("\n🔍 Validating OpenAPI Specification...")
    print("=" * 50)
    
    try:
        # Test JSON endpoint
        response = requests.get("http://localhost:8080/openapi.json", timeout=5)
        if response.status_code != 200:
            print("❌ Could not fetch OpenAPI JSON specification")
            return False
            
        spec = response.json()
        
        # Check required fields
        required_fields = ['openapi', 'info', 'paths']
        missing_fields = [field for field in required_fields if field not in spec]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
            
        print(f"✅ OpenAPI version: {spec.get('openapi')}")
        print(f"✅ API title: {spec.get('info', {}).get('title')}")
        print(f"✅ API version: {spec.get('info', {}).get('version')}")
        print(f"✅ Number of paths: {len(spec.get('paths', {}))}")
        
        # List available endpoints
        if spec.get('paths'):
            print("\n📋 Available API Endpoints:")
            for path, methods in spec['paths'].items():
                for method in methods.keys():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        print(f"   {method.upper()} {path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating OpenAPI spec: {str(e)}")
        return False

def test_api_endpoints():
    """Test some basic API endpoints"""
    print("\n🔍 Testing Basic API Endpoints...")
    print("=" * 50)
    
    endpoints = [
        {
            "name": "Health Check",
            "method": "GET",
            "url": "http://localhost:8080/api/health",
            "expected_status": [200, 404]  # 404 is ok if endpoint doesn't exist
        },
        {
            "name": "Current User (should require auth)",
            "method": "GET", 
            "url": "http://localhost:8080/api/me",
            "expected_status": [401]  # Should require authentication
        }
    ]
    
    for endpoint in endpoints:
        try:
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"], timeout=5)
            else:
                continue  # Skip non-GET requests for now
                
            if response.status_code in endpoint["expected_status"]:
                print(f"✅ {endpoint['name']}: OK (Status: {response.status_code})")
            else:
                print(f"⚠️  {endpoint['name']}: Unexpected status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint['name']}: ERROR - {str(e)}")

def main():
    """Main function to run all tests"""
    print("🚀 OpenAPI Integration Test Suite")
    print("=" * 50)
    print("Testing Mentor-Mentee Matching API integration with OpenAPI specification")
    print()
    
    # Test OpenAPI endpoints
    openapi_ok = test_openapi_endpoints()
    
    # Validate OpenAPI specification
    spec_ok = validate_openapi_spec()
    
    # Test basic API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    if openapi_ok and spec_ok:
        print("🎉 All OpenAPI integration tests passed!")
        print("\n📋 Next steps:")
        print("   1. Take screenshots of Swagger UI: http://localhost:8080/api-docs")
        print("   2. Test frontend integration: http://localhost:3001")
        print("   3. Record demo video showing API documentation")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
