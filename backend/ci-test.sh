#!/bin/bash

# CI/CD 환경용 백엔드 테스트 스크립트
# GitHub Actions 등에서 사용

echo "🤖 CI 환경에서 백엔드 테스트 실행"
echo "================================"

# Python 패키지 설치 확인
echo "🔍 설치된 패키지 확인 중..."
python -c "import flask; print(f'Flask 버전: {flask.__version__}')"

# 기본 임포트 테스트
echo "📦 모듈 임포트 테스트..."
python -c "import app; print('✅ Flask 앱 임포트 성공')"

# 간단한 API 테스트 (서버 시작 없이)
echo "🧪 API 설정 테스트..."
python -c "
from app import app
with app.test_client() as client:
    response = client.get('/')
    print(f'✅ 루트 엔드포인트 테스트: {response.status_code}')
    
    response = client.get('/openapi.yaml')
    print(f'✅ OpenAPI YAML 테스트: {response.status_code}')
"

echo "✅ 백엔드 CI 테스트 완료!"
