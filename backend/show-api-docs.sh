#!/bin/bash

# API 문서 URL 안내 스크립트

echo "📚 Mentor-Mentee API 문서 & 테스트 가이드"
echo "=============================================="
echo ""

# 서버 상태 확인
if curl -s http://localhost:8080/ &> /dev/null; then
    echo "✅ 백엔드 서버가 실행 중입니다!"
    echo ""
    
    echo "🔗 Swagger UI (인터랙티브 API 문서 & 테스트):"
    echo "   http://localhost:8080/swagger-ui"
    echo "   → API를 직접 테스트하고 요청/응답을 확인할 수 있습니다"
    echo ""
    
    echo "📄 OpenAPI 문서 (개발자용 스펙):"
    echo "   YAML: http://localhost:8080/openapi.yaml"
    echo "   JSON: http://localhost:8080/openapi.json"
    echo "   → API 스펙을 다운로드하여 개발 도구에 import 가능"
    echo ""
    
    echo "🏠 백엔드 루트:"
    echo "   http://localhost:8080/"
    echo "   → 자동으로 Swagger UI로 리다이렉트됩니다"
    echo ""
    
    echo "⚡ API 엔드포인트 베이스:"
    echo "   http://localhost:8080/api"
    echo "   → 모든 API 경로의 기본 URL"
    echo ""
    
    echo "🎯 주요 API 엔드포인트:"
    echo "   POST /api/login    - 로그인"
    echo "   POST /api/signup   - 회원가입"
    echo "   GET  /api/me       - 내 정보 조회"
    echo "   GET  /api/mentors  - 멘토 목록"
    echo "   POST /api/match-requests - 매치 요청"
    echo ""
    
    echo "🔧 사용법:"
    echo "   1. Swagger UI에서 'Authorize' 버튼 클릭"
    echo "   2. 로그인 API로 JWT 토큰 획득"
    echo "   3. 토큰을 'Bearer <token>' 형식으로 입력"
    echo "   4. 인증이 필요한 API들 테스트 가능"
    
else
    echo "❌ 백엔드 서버가 실행되지 않았습니다!"
    echo ""
    echo "백엔드를 먼저 시작해주세요:"
    echo "   ./start-backend.sh  또는  ./run-backend.sh"
    echo ""
    echo "백엔드 시작 후 다시 이 스크립트를 실행하세요."
fi

echo ""
echo "=============================================="
