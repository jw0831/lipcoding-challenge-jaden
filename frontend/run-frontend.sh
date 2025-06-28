#!/bin/bash

# 간단한 프론트엔드 실행 스크립트
# React 개발 서버를 빠르게 시작합니다.

echo "⚛️  Mentor-Mentee Frontend 서버 시작"
echo "=================================="

# 현재 디렉토리에서 실행 (이미 frontend 폴더 안에 있음)
SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR" || {
    echo "❌ 스크립트 디렉토리를 찾을 수 없습니다."
    echo "   현재 위치: $(pwd)"
    exit 1
}

# node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules가 없습니다. 전체 설정 스크립트를 사용하세요: ./start-frontend.sh"
    exit 1
fi

# React 서버 시작
echo "🚀 React 개발 서버 시작 중..."
echo ""
echo "📍 접속 정보:"
echo "   URL: http://localhost:3000"
echo ""
echo "⚡ 서버를 중지하려면 Ctrl+C"
echo "=================================="

# React 앱 실행
npm start
