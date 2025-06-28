#!/bin/bash

# Mentor-Mentee Backend 실행 스크립트
# 이 스크립트는 Flask 백엔드 서버를 시작합니다.

echo "🚀 Mentor-Mentee Backend 서버를 시작합니다..."
echo "포트: http://localhost:8080"
echo "API 문서: http://localhost:8080/swagger-ui"
echo ""

# 백엔드 디렉토리로 이동
cd "$(dirname "$0")/backend" || {
    echo "❌ backend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# Python 및 pip 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ python3이 설치되어 있지 않습니다."
    exit 1
fi

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 Python 가상환경을 생성하는 중..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 가상환경 생성에 실패했습니다."
        exit 1
    fi
fi

# 가상환경 활성화
echo "🔧 가상환경을 활성화하는 중..."
source venv/bin/activate

# 의존성 설치
if [ -f "requirements.txt" ]; then
    echo "📦 의존성 패키지를 설치하는 중..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 패키지 설치에 실패했습니다."
        exit 1
    fi
fi

# Flask 서버 시작
echo "✅ Flask 개발 서버를 시작합니다..."
echo ""
echo "📍 접속 정보:"
echo "   🏠 백엔드 메인: http://localhost:8080"
echo "   ⚡ API 엔드포인트: http://localhost:8080/api"
echo ""
echo "📚 API 문서 및 테스트:"
echo "   🔗 Swagger UI: http://localhost:8080/swagger-ui"
echo "   📄 OpenAPI YAML: http://localhost:8080/openapi.yaml"
echo "   📄 OpenAPI JSON: http://localhost:8080/openapi.json"
echo ""
echo "서버를 중지하려면 Ctrl+C를 누르세요."
echo "=================================="

python app.py
