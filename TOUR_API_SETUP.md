# 한국관광공사 Tour API 연동 가이드

Tripify에서 **실시간 축제 정보**를 사용하기 위한 한국관광공사 Tour API 설정 가이드입니다.

## 1. API 키 발급받기

### 1.1 공공데이터포털 회원가입
1. [공공데이터포털](https://www.data.go.kr/) 접속
2. 회원가입 진행 (이미 계정이 있다면 로그인)

### 1.2 API 활용신청
1. 검색창에 **"한국관광공사_국문 관광정보 서비스_GW"** 검색
2. 해당 API 선택 후 **"활용신청"** 클릭
3. 신청 정보 입력
   - 활용목적: 개인 프로젝트 / 여행 정보 제공 서비스
   - 상세설명: Tripify 여행 계획 서비스에서 축제 정보 제공
4. 신청 완료 후 **즉시 승인** (일반적으로 자동 승인)

### 1.3 API 인증키 확인
1. 마이페이지 → "오픈API" 메뉴
2. 신청한 API 목록에서 **"일반 인증키(Encoding)"** 확인
3. 인증키 복사 (예: `ABC123def456...`)

## 2. 환경변수 설정

### 2.1 .env 파일 생성
```bash
cd backend
cp .env.example .env
```

### 2.2 API 키 설정
`.env` 파일을 열고 발급받은 인증키를 입력합니다:

```env
TOUR_API_KEY=여기에_발급받은_인증키_입력
```

**주의**: `.env` 파일은 절대 GitHub에 업로드하지 마세요! (이미 .gitignore에 추가되어 있음)

## 3. 축제 데이터 동기화

### 3.1 명령줄에서 동기화

**전체 월 동기화 (1월~12월):**
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

python manage.py sync_festivals
```

**특정 월만 동기화:**
```bash
python manage.py sync_festivals --month 3  # 3월 축제만
```

**기존 데이터 삭제 후 동기화:**
```bash
python manage.py sync_festivals --clear
```

### 3.2 API 엔드포인트로 동기화

프론트엔드나 Postman에서 다음 API를 호출하여 동기화할 수 있습니다:

**전체 동기화:**
```bash
POST http://localhost:8000/api/festivals/sync/
```

**기존 데이터 삭제 후 동기화:**
```bash
POST http://localhost:8000/api/festivals/sync/?clear=true
```

**특정 월만 동기화:**
```bash
POST http://localhost:8000/api/festivals/sync/?month=5
```

**응답 예시:**
```json
{
  "message": "축제 데이터 동기화가 완료되었습니다.",
  "total_count": 245,
  "output": "1월: 20개 항목 처리 완료\n2월: 18개 항목 처리 완료\n..."
}
```

## 4. 동기화 주기 설정 (선택사항)

### 4.1 Cron Job 설정 (Linux/Mac)

매일 자정에 자동으로 축제 데이터를 업데이트하려면:

```bash
crontab -e
```

다음 라인 추가:
```cron
0 0 * * * cd /path/to/Tripify/backend && source venv/bin/activate && python manage.py sync_festivals >> /tmp/festival_sync.log 2>&1
```

### 4.2 Windows 작업 스케줄러

1. "작업 스케줄러" 실행
2. "기본 작업 만들기" 선택
3. 트리거: 매일, 시간 설정
4. 동작: 프로그램 시작
5. 프로그램: `C:\path\to\Tripify\backend\venv\Scripts\python.exe`
6. 인수: `manage.py sync_festivals`
7. 시작 위치: `C:\path\to\Tripify\backend`

## 5. 확인 및 테스트

### 5.1 데이터 확인
```bash
python manage.py shell
```

```python
from festivals.models import Festival
print(f"총 축제 수: {Festival.objects.count()}")
print(f"활성 축제 수: {Festival.objects.filter(is_active=True).count()}")

# 월별 축제 수
for month in range(1, 13):
    count = Festival.objects.filter(month=month).count()
    print(f"{month}월: {count}개")
```

### 5.2 API 테스트
```bash
# 전체 목록
curl http://localhost:8000/api/festivals/

# 월별 필터링
curl http://localhost:8000/api/festivals/?month=3

# 지역별 필터링
curl http://localhost:8000/api/festivals/?region=서울

# 검색
curl http://localhost:8000/api/festivals/?search=벚꽃
```

## 6. 문제 해결

### API 키 오류
- `.env` 파일에 API 키가 제대로 입력되었는지 확인
- API 키에 공백이나 따옴표가 없는지 확인
- 공공데이터포털에서 API가 활성화되었는지 확인

### 데이터가 없음
- 서버를 재시작했는지 확인
- `sync_festivals` 명령을 실행했는지 확인
- API 응답을 확인: 로그에서 오류 메시지 확인

### 인코딩 오류
- API 키는 **일반 인증키 (Encoding)** 사용
- 디코딩 키가 아닌 인코딩된 키 사용

## 7. API 사용량 제한

한국관광공사 API는 다음과 같은 제한이 있습니다:
- 일일 호출 제한: 1,000건
- 트래픽 제한: 충분히 여유 있음

따라서:
- 실시간 호출보다는 **주기적 동기화 방식** 권장
- 하루 1-2회 동기화로 충분
- 데이터베이스에 캐싱하여 사용

## 8. 프론트엔드 통합

동기화된 데이터는 기존 API 엔드포인트에서 그대로 사용할 수 있습니다:

```javascript
// 축제 목록 가져오기
const response = await axios.get('http://localhost:8000/api/festivals/')

// 이제 실시간 API에서 가져온 수백 개의 축제 데이터가 표시됩니다!
```

## 참고 자료

- [공공데이터포털](https://www.data.go.kr/)
- [한국관광공사 Tour API 문서](https://www.data.go.kr/data/15101578/openapi.do)
- [Django Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)

---

**완료!** 이제 Tripify에서 실시간 축제 정보를 사용할 수 있습니다! 🎉
