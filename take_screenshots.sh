#!/bin/bash

# 📸 멘토-멘티 앱 스크린샷 자동 촬영 스크립트
# 이 스크립트는 각 페이지를 순서대로 열어 스크린샷 촬영을 도와줍니다.

echo "🎯 멘토-멘티 앱 스크린샷 촬영 가이드"
echo "======================================"
echo ""

# 스크린샷 디렉토리 생성
SCREENSHOT_DIR="docs/screenshots"
mkdir -p "$SCREENSHOT_DIR"

echo "📁 스크린샷 저장 위치: $SCREENSHOT_DIR"
echo ""

# 서버 상태 확인
echo "🔍 서버 상태 확인 중..."
echo ""

# 백엔드 확인
if curl -s http://localhost:8080/api/health > /dev/null 2>&1; then
    echo "✅ 백엔드 서버: http://localhost:8080 (실행 중)"
else
    echo "❌ 백엔드 서버: http://localhost:8080 (중지됨)"
    echo "   백엔드를 시작하세요: cd backend && source venv/bin/activate && python app.py"
fi

# 프론트엔드 확인
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ 프론트엔드 서버: http://localhost:3001 (실행 중)"
else
    echo "❌ 프론트엔드 서버: http://localhost:3001 (중지됨)"
    echo "   프론트엔드를 시작하세요: cd frontend && PORT=3001 npm start"
fi

echo ""
echo "🎥 스크린샷 촬영 가이드"
echo "======================"

# 스크린샷 목록
screenshots=(
    "01-login-page.png|http://localhost:3001|로그인 페이지 - 앱의 첫 화면"
    "02-signup-page.png|http://localhost:3001|회원가입 페이지 - Sign Up 버튼 클릭 후"
    "03-profile-page.png|http://localhost:3001|프로필 페이지 - 로그인 후 Profile 클릭"
    "04-mentor-list.png|http://localhost:3001|멘토 목록 페이지 - Mentors 클릭"
    "05-match-requests.png|http://localhost:3001|매칭 요청 페이지 - Requests 클릭"
    "06-api-docs.png|http://localhost:8080/api-docs|API 문서 - Swagger UI"
)

for i in "${!screenshots[@]}"; do
    IFS='|' read -r filename url description <<< "${screenshots[$i]}"
    echo ""
    echo "📸 스크린샷 $((i+1))/6: $filename"
    echo "   URL: $url"
    echo "   설명: $description"
    echo ""
    echo "   📋 다음 단계:"
    echo "   1. 위 URL을 브라우저에서 열기"
    echo "   2. 페이지가 완전히 로드될 때까지 대기"
    echo "   3. Cmd + Shift + 4로 화면 캡처"
    echo "   4. 캡처한 이미지를 $SCREENSHOT_DIR/$filename 으로 저장"
    echo ""
    
    # URL 자동으로 열기 (선택사항)
    read -p "   🌐 브라우저에서 이 URL을 자동으로 열까요? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$url"
        echo "   ✅ 브라우저에서 $url 을 열었습니다."
    fi
    
    echo ""
    read -p "   ⏸️  스크린샷을 촬영했으면 Enter를 눌러 계속하세요..."
done

echo ""
echo "🎉 모든 스크린샷 촬영이 완료되었습니다!"
echo ""
echo "📋 다음 단계:"
echo "1. docs/screenshots/ 폴더에 모든 이미지가 저장되었는지 확인"
echo "2. 데모 비디오 녹화 (SUBMISSION_GUIDE.md 참고)"
echo "3. YouTube에 비디오 업로드"
echo "4. README.md 업데이트"
echo "5. GitHub에 최종 커밋 및 푸시"
echo ""
echo "📁 촬영된 스크린샷 확인:"
ls -la "$SCREENSHOT_DIR"
