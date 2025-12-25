#!/bin/bash
set -e  # 에러 발생 시 스크립트 중단

echo "=========================================="
echo "Tripify Backend Build Script"
echo "=========================================="

# 1. 의존성 설치
echo ""
echo "[1/5] Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# 2. Static 파일 수집
echo ""
echo "[2/5] Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"

# 3. 데이터베이스 마이그레이션
echo ""
echo "[3/5] Running database migrations..."
python manage.py migrate
echo "✓ Migrations completed"

# 4. 장소 데이터 로드
echo ""
echo "[4/5] Loading place data..."
python manage.py load_places
echo "✓ Place data loaded"

# 5. 축제 데이터 로드
echo ""
echo "[5/5] Loading festival data..."
python manage.py load_festivals
echo "✓ Festival data loaded"

echo ""
echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="

