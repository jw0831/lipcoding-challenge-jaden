# 🎥 YouTube 업로드 가이드

## 📋 YouTube 업로드 체크리스트

### 1. 비디오 녹화 완료 확인
- [ ] 비디오 길이: 5-10분
- [ ] 모든 주요 기능 시연 포함
- [ ] 음성 품질 양호
- [ ] 화면 해상도 적절 (최소 720p)

### 2. YouTube 채널 준비
- [ ] YouTube 계정 로그인
- [ ] 채널 이름 확인 (개인 또는 프로젝트용)

---

## 📤 업로드 단계별 가이드

### Step 1: YouTube Studio 접속
1. https://studio.youtube.com 접속
2. "만들기" → "동영상 업로드" 클릭

### Step 2: 동영상 파일 업로드
1. 녹화한 비디오 파일 선택
2. 업로드 진행률 확인

### Step 3: 기본 정보 입력

#### 제목 (Title)
```
멘토-멘티 매칭 웹 애플리케이션 데모 - React & Flask Full Stack Project
```

#### 설명 (Description)
```
🎯 멘토-멘티 매칭 웹 애플리케이션 데모

이 프로젝트는 React와 Flask를 사용하여 구축한 풀스택 웹 애플리케이션입니다.
멘티와 멘토를 연결해주는 매칭 플랫폼으로, 실제 비즈니스 요구사항을 반영한 완전한 기능을 제공합니다.

🔧 기술 스택:
• Frontend: React 18, Context API, Axios, CSS3
• Backend: Flask, SQLAlchemy ORM, JWT Authentication
• Database: SQLite
• Testing: PyTest (TDD 방식)
• API Documentation: OpenAPI/Swagger UI

🌟 주요 기능:
• 사용자 인증 시스템 (JWT 기반)
• 역할 기반 접근 제어 (멘토/멘티)
• 프로필 관리 (이미지 업로드 포함)
• 멘토 검색 및 필터링
• 실시간 매칭 요청 시스템
• RESTful API 설계
• 완전한 TDD 테스트 커버리지

📁 GitHub Repository: https://github.com/[YOUR_USERNAME]/mentor-mentee-app

⏱️ 타임스탬프:
00:00 - 프로젝트 소개
00:30 - 회원가입 및 로그인
01:30 - 프로필 관리
02:30 - 멘토 탐색 및 검색
04:00 - 매칭 요청 시스템
05:30 - API 문서 및 코드 구조

🏷️ 태그: #React #Flask #FullStack #WebDevelopment #Portfolio #JavaScript #Python #API #JWT #TDD
```

#### 썸네일
- 자동 생성된 썸네일 중 선택
- 또는 커스텀 썸네일 업로드 (1280x720 권장)

### Step 4: 공개 설정

#### 권장 설정:
- **공개 범위**: "링크를 아는 모든 사용자"
- **이유**: 포트폴리오용이므로 링크로만 접근 가능하게 설정

#### 대안:
- **공개**: 완전 공개 (검색 가능)
- **비공개**: 본인만 시청 가능

### Step 5: 고급 설정

#### 카테고리
- "과학/기술" 선택

#### 언어
- "한국어" 또는 "영어" (비디오 언어에 따라)

#### 댓글 설정
- "모든 댓글 허용" (피드백 받기 위해)

---

## 📋 업로드 후 해야 할 일

### 1. 비디오 링크 복사
업로드 완료 후 비디오 URL 복사:
```
https://youtu.be/[VIDEO_ID]
```

### 2. README.md 업데이트
```markdown
## 🎥 Demo Video
[![Demo Video](https://img.youtube.com/vi/[VIDEO_ID]/0.jpg)](https://youtu.be/[VIDEO_ID])

[▶️ Watch Full Demo on YouTube](https://youtu.be/[VIDEO_ID])
```

### 3. GitHub 커밋
```bash
git add README.md
git commit -m "docs: Add YouTube demo video link"
git push origin main
```

---

## 💡 YouTube 최적화 팁

### 썸네일 최적화
- 명확한 제목 텍스트 추가
- 밝고 대비가 좋은 색상 사용
- 앱 스크린샷 포함

### SEO 최적화
- 제목에 핵심 키워드 포함
- 해시태그 적절히 사용
- 상세한 설명 작성

### 접근성
- 자막 추가 (YouTube 자동 생성 또는 수동)
- 챕터 나누기 (긴 비디오의 경우)

---

## 🔧 문제 해결

### 업로드 실패 시
1. 파일 크기 확인 (YouTube 한도: 128GB)
2. 비디오 형식 확인 (MP4 권장)
3. 인터넷 연결 상태 확인

### 화질 문제
- 업로드 후 처리 시간 필요 (HD 품질까지 수 분 소요)
- 원본 비디오 해상도 확인

### 저작권 문제
- 배경음악 사용 시 저작권 확인
- 무료 음원 사용 권장

---

## ✅ 최종 체크리스트

- [ ] 비디오 업로드 완료
- [ ] 제목/설명 최적화
- [ ] 적절한 공개 설정
- [ ] 썸네일 설정
- [ ] 비디오 URL 복사
- [ ] README.md 업데이트
- [ ] GitHub 푸시 완료

**성공적인 YouTube 업로드를 위해 각 단계를 꼼꼼히 확인하세요! 🚀**
