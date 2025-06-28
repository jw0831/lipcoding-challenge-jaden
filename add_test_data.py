#!/usr/bin/env python3
"""
데이터베이스에 테스트 데이터를 추가하는 스크립트
"""

import requests
import json

# 서버 URL
BASE_URL = "http://localhost:8080"

def create_test_users():
    """테스트 사용자들을 생성합니다"""
    
    # 추가 멘토 생성
    mentors = [
        {
            "email": "alice.smith@test.com",
            "password": "password123",
            "role": "mentor",
            "name": "Alice Smith",
            "bio": "Senior Full-Stack Developer with 8 years of experience in React, Node.js, and Python",
            "skills": ["React", "Node.js", "Python", "AWS", "MongoDB"]
        },
        {
            "email": "bob.jones@test.com", 
            "password": "password123",
            "role": "mentor",
            "name": "Bob Jones",
            "bio": "DevOps Engineer specializing in cloud infrastructure and CI/CD pipelines",
            "skills": ["Docker", "Kubernetes", "AWS", "Jenkins", "Terraform"]
        },
        {
            "email": "carol.white@test.com",
            "password": "password123", 
            "role": "mentor",
            "name": "Carol White",
            "bio": "Data Scientist with expertise in Machine Learning and AI",
            "skills": ["Python", "TensorFlow", "Pandas", "SQL", "Machine Learning"]
        },
        {
            "email": "david.brown@test.com",
            "password": "password123",
            "role": "mentor", 
            "name": "David Brown",
            "bio": "Mobile App Developer with experience in iOS and Android development",
            "skills": ["Swift", "Kotlin", "React Native", "Flutter", "Firebase"]
        },
        {
            "email": "eva.green@test.com",
            "password": "password123",
            "role": "mentor",
            "name": "Eva Green", 
            "bio": "UI/UX Designer and Frontend Developer",
            "skills": ["Figma", "React", "CSS", "JavaScript", "Design Systems"]
        }
    ]
    
    # 추가 멘티 생성
    mentees = [
        {
            "email": "john.doe@test.com",
            "password": "password123",
            "role": "mentee",
            "name": "John Doe",
            "bio": "Computer Science student looking to learn web development"
        },
        {
            "email": "jane.wilson@test.com", 
            "password": "password123",
            "role": "mentee",
            "name": "Jane Wilson",
            "bio": "Career changer interested in data science and analytics"
        },
        {
            "email": "mike.taylor@test.com",
            "password": "password123",
            "role": "mentee", 
            "name": "Mike Taylor",
            "bio": "Junior developer wanting to improve backend skills"
        },
        {
            "email": "sarah.davis@test.com",
            "password": "password123",
            "role": "mentee",
            "name": "Sarah Davis", 
            "bio": "Designer looking to transition into frontend development"
        }
    ]
    
    all_users = mentors + mentees
    created_users = []
    
    for user in all_users:
        try:
            # 회원가입
            signup_data = {
                "email": user["email"],
                "password": user["password"], 
                "role": user["role"],
                "name": user["name"]
            }
            
            response = requests.post(f"{BASE_URL}/api/signup", 
                                   headers={"Content-Type": "application/json"},
                                   json=signup_data)
            
            if response.status_code == 201:
                print(f"✅ Created user: {user['email']}")
                
                # 로그인해서 토큰 획득
                login_data = {
                    "email": user["email"],
                    "password": user["password"]
                }
                
                login_response = requests.post(f"{BASE_URL}/api/login",
                                             headers={"Content-Type": "application/json"},
                                             json=login_data)
                
                if login_response.status_code == 200:
                    token = login_response.json()["token"]
                    
                    # 프로필 업데이트
                    profile_data = {
                        "name": user["name"],
                        "bio": user["bio"]
                    }
                    
                    # 멘토의 경우 스킬 추가
                    if user["role"] == "mentor" and "skills" in user:
                        profile_data["skills"] = user["skills"]
                    
                    profile_response = requests.put(f"{BASE_URL}/api/me",
                                                  headers={
                                                      "Content-Type": "application/json",
                                                      "Authorization": f"Bearer {token}"
                                                  },
                                                  json=profile_data)
                    
                    if profile_response.status_code == 200:
                        print(f"   📝 Updated profile for: {user['email']}")
                        created_users.append({
                            "email": user["email"],
                            "role": user["role"],
                            "token": token
                        })
                    else:
                        print(f"   ❌ Failed to update profile for: {user['email']}")
                else:
                    print(f"   ❌ Failed to login: {user['email']}")
            elif response.status_code == 400 and "already exists" in response.text:
                print(f"⚠️  User already exists: {user['email']}")
            else:
                print(f"❌ Failed to create user: {user['email']} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating user {user['email']}: {e}")
    
    return created_users

def verify_data():
    """생성된 데이터를 확인합니다"""
    
    # 테스트 사용자로 로그인
    login_data = {"email": "user@test.com", "password": "user"}
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", 
                               headers={"Content-Type": "application/json"},
                               json=login_data)
        
        if response.status_code == 200:
            token = response.json()["token"]
            
            # 멘토 목록 조회
            mentors_response = requests.get(f"{BASE_URL}/api/mentors",
                                          headers={"Authorization": f"Bearer {token}"})
            
            if mentors_response.status_code == 200:
                mentors = mentors_response.json()
                print(f"\n📊 Total mentors available: {len(mentors)}")
                
                for mentor in mentors:
                    skills = mentor.get("profile", {}).get("skills", [])
                    print(f"   - {mentor.get('profile', {}).get('name', 'Unknown')}: {', '.join(skills) if skills else 'No skills listed'}")
            else:
                print(f"❌ Failed to fetch mentors: {mentors_response.text}")
        else:
            print(f"❌ Failed to login with test user: {response.text}")
            
    except Exception as e:
        print(f"❌ Error verifying data: {e}")

def main():
    """메인 함수"""
    print("🚀 Adding test data to the database...")
    print(f"Server URL: {BASE_URL}")
    
    # 서버 연결 확인
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Backend server is running")
    except Exception as e:
        print(f"❌ Backend server is not accessible: {e}")
        return
    
    # 테스트 사용자 생성
    created_users = create_test_users()
    
    print(f"\n📈 Summary:")
    print(f"   - Created {len(created_users)} new users")
    
    # 데이터 확인
    verify_data()
    
    print("\n🎉 Test data setup complete!")
    print("Now you can test the application with multiple mentors and mentees.")

if __name__ == "__main__":
    main()
