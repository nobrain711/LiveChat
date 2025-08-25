# test_health.py
# health endpoint 테스트
# v1.0

# 패키지 호출
import pytest # test모듈
from httpx import AsyncClient # 비동기 HTTP 클라이언트
from fastapi import status # HTTP 상태 코드

pytestmark = pytest.mark.asyncio # 비동기 테스트 마크

async def test_health_check(client: AsyncClient) -> None:
  '''
  헬스 체크 엔드포인트 테스트
  /health 엔트포인트가 성공적으로 DB 연결을 확인하는 경우
  '''
  # 헬스 체크 엔드포인트에 GET 요청을 보내고 응답을 확인
  response = await client.get("/health")
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {"status": "healthy"}
  
async def test_health_check_db_failure(monkeypatch, client: AsyncClient) -> None:
  '''
  헬스 체크 엔드포인트 테스트
  /health 엔트포인트가 DB 연결 실패를 처리하는 경우
  '''

  def mock_execute_raise_exception(*args, **kwargs):
      raise Exception("DB connection failed for test")

  monkeypatch.setattr("app.db.execute", lambda _: mock_execute_raise_exception())

  # 헬스 체크 엔드포인트에 GET 요청을 보내고 응답을 확인
  response = await client.get("/health")
  
  # 503 error 확인
  assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
  assert 'Database connection failed for test' in response.json()['detail']