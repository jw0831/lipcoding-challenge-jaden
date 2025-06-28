# 📋 멘토-멘티 매칭 앱 제출 가이드

## 🎯 제출 요구사항 체크리스트

### ✅ 완료된 항목
- [x] 백엔드 API 구현 (Flask + SQLite)
- [x] 프론트엔드 UI 구현 (React)
- [x] 모든 기능 구현 (인증, 프로필, 매칭, 요청 관리)
- [x] TDD 테스트 스위트 작성 및 통과
- [x] GitHub 레포지토리 생성 및 코드 푸시
- [x] API 문서 (OpenAPI/Swagger)

### 🔄 진행 중인 항목
- [ ] 앱 스크린샷 촬영 및 업로드
- [ ] 데모 비디오 녹화 및 YouTube 업로드
- [ ] README 업데이트

---

## 📸 1단계: 스크린샷 촬영하기

### 현재 실행 중인 서버
- **백엔드**: http://localhost:8080
- **프론트엔드**: http://localhost:3001
- **API 문서**: http://localhost:8080/api-docs

### 촬영해야 할 스크린샷 목록

#### 1. 홈/로그인 페이지
- 파일명: `01-login-page.png`
- URL: http://localhost:3001
- 설명: 앱의 첫 화면, 로그인 폼

#### 2. 회원가입 페이지
- 파일명: `02-signup-page.png`
- URL: http://localhost:3001 (Sign Up 클릭)
- 설명: 회원가입 폼

#### 3. 프로필 페이지 (로그인 후)
- 파일명: `03-profile-page.png`
- 설명: 사용자 프로필 정보 및 편집 기능

#### 4. 멘토 목록 페이지
- 파일명: `04-mentor-list.png`
- 설명: 멘토들의 리스트, 필터링/정렬 기능

#### 5. 매칭 요청 페이지
- 파일명: `05-match-requests.png`
- 설명: 보낸/받은 요청 목록

#### 6. API 문서 페이지
- 파일명: `06-api-docs.png`
- URL: http://localhost:8080/api-docs
- 설명: Swagger UI API 문서

### 스크린샷 촬영 방법 (macOS)

1. **전체 화면 캡처**: `Cmd + Shift + 3`
2. **선택 영역 캡처**: `Cmd + Shift + 4`
3. **특정 창 캡처**: `Cmd + Shift + 4` 후 스페이스바

### 스크린샷 저장 위치
```bash
/Users/jaden/code_collec/lib_coding_challenge/docs/screenshots/
```

---

## 🎥 2단계: 데모 비디오 녹화하기

### 비디오 시나리오 (5-10분)

1. **인트로** (30초)
   - "안녕하세요, 멘토-멘티 매칭 앱을 소개합니다"
   - 기술 스택 간단 소개 (React, Flask, SQLite, JWT)

2. **회원가입 및 로그인** (1분)
   - 새 계정 생성
   - 로그인 과정 시연

3. **프로필 설정** (1분)
   - 프로필 정보 입력/수정
   - 프로필 이미지 업로드 (선택사항)

4. **멘토 탐색** (2분)
   - 멘토 목록 보기
   - 필터링 및 정렬 기능 시연
   - 멘토 상세 정보 확인

5. **매칭 요청** (2분)
   - 멘토에게 요청 보내기
   - 다른 계정으로 로그인하여 요청 수락/거절
   - 요청 상태 확인

6. **API 문서** (1분)
   - Swagger UI 시연
   - 주요 엔드포인트 설명

7. **코드 구조** (1-2분)
   - GitHub 레포지토리 구조 소개
   - 주요 파일들 간단 설명

### 비디오 녹화 도구 추천

#### macOS 기본 도구
```bash
# QuickTime Player 사용
# 또는 Command + Shift + 5로 화면 녹화
```

#### 전문 도구 (선택사항)
- **OBS Studio** (무료): https://obsproject.com/
- **ScreenFlow** (유료): https://www.telestream.net/screenflow/
- **Loom** (온라인): https://www.loom.com/

---

## 📤 3단계: YouTube 업로드

### 업로드 설정
- **제목**: "멘토-멘티 매칭 웹 애플리케이션 데모 - React & Flask"
- **설명**: 
  ```
  멘토-멘티 매칭 웹 애플리케이션 데모입니다.
  
  🔧 기술 스택:
  - Frontend: React, Context API, Axios
  - Backend: Flask, SQLAlchemy, JWT
  - Database: SQLite
  - Testing: PyTest (TDD)
  
  🌟 주요 기능:
  - 사용자 인증 (회원가입/로그인)
  - 프로필 관리
  - 멘토 검색 및 필터링
  - 매칭 요청 시스템
  - API 문서 (Swagger UI)
  
  📁 GitHub: [여기에 GitHub 링크 추가]
  ```
- **공개 설정**: "비공개" 또는 "링크가 있는 사용자만"
- **태그**: React, Flask, WebDevelopment, FullStack, API

---

## 📝 4단계: README.md 업데이트

현재 제공된 `README_TEMPLATE.md`를 사용하여 메인 `README.md`를 업데이트하세요:

```bash
cp README_TEMPLATE.md README.md
# 그 후 스크린샷과 YouTube 링크 추가
```

### 추가해야 할 내용
1. YouTube 비디오 링크
2. 스크린샷 이미지들
3. 설치 및 실행 가이드
4. API 엔드포인트 요약

---

## 🚀 5단계: 최종 GitHub 커밋

```bash
# 스크린샷 추가
git add docs/screenshots/*.png

# README 업데이트 후
git add README.md

# 최종 커밋
git commit -m "docs: Add screenshots and demo video for submission"

# GitHub에 푸시
git push origin main
```

---

## ✅ 제출 전 최종 체크리스트

- [ ] 모든 스크린샷이 docs/screenshots/ 폴더에 저장됨
- [ ] YouTube 비디오가 업로드되고 링크가 작동함
- [ ] README.md가 완전히 업데이트됨
- [ ] GitHub 레포지토리가 최신 상태로 푸시됨
- [ ] 앱이 정상적으로 실행됨 (포트 확인)
- [ ] 모든 주요 기능이 작동함

---

## 📞 문제 해결

### 서버 재시작이 필요한 경우
```bash
# 백엔드 재시작
cd backend && source venv/bin/activate && python app.py

# 프론트엔드 재시작 (다른 터미널에서)
cd frontend && PORT=3001 npm start
```

### 포트 충돌 해결
```bash
# 포트 사용 중인 프로세스 찾기
lsof -ti:3001 | xargs kill -9  # 프론트엔드
lsof -ti:8080 | xargs kill -9  # 백엔드
```

---

**성공적인 제출을 위해 각 단계를 차근차근 따라해주세요! 🎉**
