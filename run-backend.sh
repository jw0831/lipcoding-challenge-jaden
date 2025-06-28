#!/bin/bash

# 간단한 백엔드 실행 스크립트
# Flask API 서버를 빠르게 시작합니다.

echo "🔥 Mentor-Mentee Backend 서버 시작"
echo "=================================="

# 백엔드 디렉토리로 이동
cd backend 2>/dev/null || {
    echo "❌ backend 폴더를 찾을 수 없습니다."
    echo "   현재 위치: $(pwd)"
    exit 1
}

# 가상환경 활성화
if [ -d "venv" ]; then
    echo "🔧 가상환경 활성화..."
    source venv/bin/activate
else
    echo "⚠️  가상환경이 없습니다. 전체 설정 스크립트를 사용하세요: ./start-backend.sh"
    exit 1
fi

# Flask 서버 시작
echo "🚀 Flask 서버 시작 중..."
echo ""
echo "📍 접속 정보:"
echo "   🏠 메인: http://localhost:8080"
echo "   ⚡ API: http://localhost:8080/api"
echo ""
echo "📚 API 문서:"
echo "   🔗 Swagger UI: http://localhost:8080/swagger-ui"
echo "   📄 OpenAPI YAML: http://localhost:8080/openapi.yaml"
echo "   📄 OpenAPI JSON: http://localhost:8080/openapi.json"
echo ""
echo "⚡ 서버를 중지하려면 Ctrl+C"
echo "=================================="

# Flask 앱 실행
python app.py
