#!/bin/bash

# Mentor-Mentee 전체 애플리케이션 실행 스크립트
# 이 스크립트는 백엔드와 프론트엔드를 모두 시작합니다.

echo "🚀 Mentor-Mentee 애플리케이션을 시작합니다..."
echo ""

# 현재 스크립트의 디렉토리로 이동
cd "$(dirname "$0")" || {
    echo "❌ 스크립트 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 터미널 지원 확인
if ! command -v osascript &> /dev/null && ! command -v gnome-terminal &> /dev/null; then
    echo "⚠️  새 터미널 창을 자동으로 열 수 없습니다."
    echo "수동으로 백엔드와 프론트엔드를 실행해주세요:"
    echo ""
    echo "백엔드: ./start-backend.sh"
    echo "프론트엔드: ./start-frontend.sh"
    exit 1
fi

# 스크립트 실행 권한 부여
chmod +x start-backend.sh
chmod +x start-frontend.sh

echo "1️⃣  백엔드 서버를 시작합니다..."

# macOS의 경우
if [[ "$OSTYPE" == "darwin"* ]]; then
    # 백엔드를 새 터미널 탭에서 실행
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && ./start-backend.sh\""
    
    # 프론트엔드 시작 전 잠시 대기
    echo "⏳ 백엔드 서버 시작을 기다리는 중 (5초)..."
    sleep 5
    
    echo "2️⃣  프론트엔드 서버를 시작합니다..."
    # 프론트엔드를 새 터미널 탭에서 실행
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && ./start-frontend.sh\""
    
# Linux의 경우
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # 백엔드를 새 터미널에서 실행
    gnome-terminal -- bash -c "cd $(pwd) && ./start-backend.sh; exec bash"
    
    # 프론트엔드 시작 전 잠시 대기
    echo "⏳ 백엔드 서버 시작을 기다리는 중 (5초)..."
    sleep 5
    
    echo "2️⃣  프론트엔드 서버를 시작합니다..."
    # 프론트엔드를 새 터미널에서 실행
    gnome-terminal -- bash -c "cd $(pwd) && ./start-frontend.sh; exec bash"
fi

echo ""
echo "✅ 애플리케이션 시작 완료!"
echo ""
echo "📌 접속 정보:"
echo "   🖥️  프론트엔드: http://localhost:3000"
echo "   🖥️  백엔드: http://localhost:8080"
echo ""
echo "📚 API 문서 및 테스트:"
echo "   🔗 Swagger UI: http://localhost:8080/swagger-ui"
echo "   📄 OpenAPI YAML: http://localhost:8080/openapi.yaml"
echo "   📄 OpenAPI JSON: http://localhost:8080/openapi.json"
echo ""
echo "📋 테스트 사용자:"
echo "   👤 멘티: user@test.com / user"
echo "   👤 멘토: mentor@test.com / user"
echo ""
echo "🛑 서버를 중지하려면 각 터미널에서 Ctrl+C를 누르세요."
