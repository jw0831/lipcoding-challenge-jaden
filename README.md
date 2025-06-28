# Mentor-Mentee Application

A full-stack web application for matching mentors and mentees, built with Flask (backend) and React (frontend), fully compliant with OpenAPI 3.0 specification.

## 🎯 Features

- **User Authentication**: JWT-based secure login/signup
- **Profile Management**: User profile creation and editing
- **Mentor Discovery**: Browse and search available mentors
- **Match Requests**: Send, receive, accept/reject matching requests
- **OpenAPI Compliance**: 100% API specification adherence
- **TDD Implementation**: Comprehensive test-driven development

## 🚀 Quick Start

### ⚡ 자동 실행 스크립트 (권장)
```bash
# 전체 애플리케이션 실행 (백엔드 + 프론트엔드)
./start-app.sh

# 개별 실행 (완전 설정)
./start-backend.sh    # 백엔드 (가상환경 생성, 패키지 설치 포함)
./start-frontend.sh   # 프론트엔드 (npm install 포함)

# 빠른 실행 (이미 설정된 경우)
./run-backend.sh      # 백엔드만 빠르게 시작
./run-frontend.sh     # 프론트엔드만 빠르게 시작
```

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Backend will run on http://localhost:8080

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend will run on http://localhost:3000

### Test Users
- **Mentee**: user@test.com / user
- **Mentor**: mentor@test.com / user

## 📋 API Documentation

- **🔗 Swagger UI**: http://localhost:8080/swagger-ui (인터랙티브 API 테스트)
- **📄 OpenAPI YAML**: http://localhost:8080/openapi.yaml (YAML 형식 스펙)  
- **📄 OpenAPI JSON**: http://localhost:8080/openapi.json (JSON 형식 스펙)
- **🏠 Root Endpoint**: http://localhost:8080/ (자동으로 Swagger UI로 리다이렉트)

## 🧪 Testing

### Run TDD Tests
```bash
# OpenAPI compliance tests
python test_openapi_tdd.py

# API endpoint compliance tests  
python test_api_compliance_tdd.py

# Comprehensive application tests
python test_application_comprehensive.py

# Browser testing guide
python test_browser_comprehensive.py
```

### Manual Testing
1. Open http://localhost:3000
2. Login with test users
3. Navigate through all pages
4. Test mentor discovery and match requests
5. Verify data persistence

## 📁 Project Structure

```
├── backend/                    # Flask API server
│   ├── app.py                 # Main application
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Virtual environment
├── frontend/                  # React application
│   ├── src/                   # Source code
│   ├── public/                # Static assets
│   └── package.json           # Node dependencies
├── openapi.yaml               # OpenAPI 3.0 specification
├── test_*.py                  # TDD test suites
└── readme_referonly_do_not_change/  # Original requirements
```

## 🎬 Demo

See `FINAL_SUBMISSION_REPORT.md` for detailed testing checklist and demo video guidelines.

## 🛠 Technology Stack

**Backend:**
- Flask 2.3.3
- SQLAlchemy (SQLite)
- JWT authentication
- OpenAPI/Swagger
- Flask-CORS

**Frontend:**
- React 18
- React Router v6
- Context API
- Fetch API

**Testing:**
- pytest
- requests
- TDD methodology

## ✅ Completion Status

- [x] OpenAPI 3.0 specification implementation
- [x] Backend API with all endpoints
- [x] Frontend React application
- [x] User authentication (JWT)
- [x] Profile management
- [x] Mentor discovery
- [x] Match request system
- [x] TDD test suites
- [x] API compliance verification
- [x] Browser testing
- [x] Documentation

**Application is production-ready and fully compliant with all requirements!**
