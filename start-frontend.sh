#!/bin/bash

# Mentor-Mentee Frontend 실행 스크립트
# 이 스크립트는 React 프론트엔드 서버를 시작합니다.

echo "🚀 Mentor-Mentee Frontend 서버를 시작합니다..."
echo "포트: http://localhost:3000"
echo ""

# 프론트엔드 디렉토리로 이동
cd "$(dirname "$0")/frontend" || {
    echo "❌ frontend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# Node.js 및 npm 설치 확인
if ! command -v npm &> /dev/null; then
    echo "❌ npm이 설치되어 있지 않습니다. Node.js를 설치해주세요."
    exit 1
fi

# package.json 확인
if [ ! -f "package.json" ]; then
    echo "❌ package.json 파일을 찾을 수 없습니다."
    exit 1
fi

# 의존성 설치 확인
if [ ! -d "node_modules" ]; then
    echo "📦 의존성 패키지를 설치하는 중..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 패키지 설치에 실패했습니다."
        exit 1
    fi
fi

# React 개발 서버 시작
echo "✅ React 개발 서버를 시작합니다..."
echo "브라우저에서 http://localhost:3000 으로 접속하세요."
echo ""
echo "서버를 중지하려면 Ctrl+C를 누르세요."
echo "=================================="

npm start
