# 멘토-멘티 매칭 애플리케이션

이 애플리케이션은 멘토와 멘티를 매칭하는 웹 애플리케이션입니다. Python Flask 백엔드와 React 프론트엔드로 구성되어 있습니다.

## 🚀 빠른 시작

### 자동 시작 (권장)

```bash
./start.sh
```

### 수동 시작

#### 백엔드 서버 시작

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### 프론트엔드 서버 시작 (새 터미널에서)

```bash
cd frontend
npm install
npm start
```

## 📍 접속 정보

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8080/api
- **Swagger UI**: http://localhost:8080/swagger-ui
- **OpenAPI 스펙**: http://localhost:8080/openapi.json

## 🛠️ 기술 스택

### 백엔드
- Python 3.x
- Flask
- Flask-SQLAlchemy (SQLite 데이터베이스)
- Flask-JWT-Extended (JWT 인증)
- Flask-CORS
- Pillow (이미지 처리)

### 프론트엔드
- React 18
- React Router DOM
- Axios (HTTP 클라이언트)
- Modern CSS

## 📋 주요 기능

### 1. 사용자 관리
- 회원가입 (멘토/멘티 역할 선택)
- 로그인/로그아웃
- JWT 기반 인증

### 2. 프로필 관리
- 프로필 정보 수정 (이름, 소개글)
- 프로필 이미지 업로드
- 멘토 기술 스택 관리

### 3. 멘토 검색 (멘티용)
- 멘토 목록 조회
- 기술 스택으로 필터링
- 이름/기술 스택으로 정렬

### 4. 매칭 요청 시스템
- 멘티가 멘토에게 매칭 요청 전송
- 멘토가 요청 수락/거절
- 요청 상태 관리 (대기중/수락/거절)

### 5. 요청 관리
- 멘티: 보낸 요청 조회 및 삭제
- 멘토: 받은 요청 조회 및 응답

## 🔐 보안 기능

- JWT 토큰 기반 인증
- 비밀번호 해싱
- 파일 업로드 검증
- SQL 인젝션 방지
- XSS 공격 방지

## 📊 데이터베이스 스키마

### Users 테이블
- id (Primary Key)
- email (Unique)
- password_hash
- role (mentor/mentee)
- name
- bio
- profile_image
- created_at

### MentorSkills 테이블
- id (Primary Key)
- user_id (Foreign Key)
- skill

### MatchingRequests 테이블
- id (Primary Key)
- mentor_id (Foreign Key)
- mentee_id (Foreign Key)
- message
- status (pending/accepted/rejected)
- created_at
- updated_at

## 🧪 테스트 사용자

애플리케이션을 테스트하려면 다음과 같이 사용자를 생성하세요:

1. 멘토 계정 생성 (기술 스택 추가)
2. 멘티 계정 생성
3. 멘티로 로그인하여 멘토 검색 및 요청 전송
4. 멘토로 로그인하여 요청 수락/거절

## 📝 API 문서

상세한 API 문서는 애플리케이션 실행 후 http://localhost:8080/swagger-ui 에서 확인할 수 있습니다.

## 🔧 개발 환경

- Python 3.8+
- Node.js 16+
- npm 또는 yarn

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.
