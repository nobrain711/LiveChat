# conftest.py
# /health endpoint 실행 확인

# 패키지 호출
import pytest # test모듈
from typing import AsyncGenerator # 
from fastapi import FastAPI # FastAPI
from httpx import AsyncClient # 비동기 HTTP 클라이언트
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # 비동기 세션
from sqlalchemy.orm import sessionmaker # 세션 메이커

# 테스트 모듈 호출
from app.db import get_db_session # DB 세션 가져오기
from main import app as fastapi_app # FastAPI 앱 가져오기
from core import settings # 설정 가져오기

# test용 비동기 DB 엔진 생성
test_engine = create_async_engine(
  bind=settings.DATABASE_URL, # DB URL
)

# test용 비동기 세션 생성
test_async_session_local = sessionmaker(
  bind=test_engine,         # DB 엔진
  class_=AsyncSession,      # 비동기 세션 클래스
  autocommit=False,         # 자동 커밋 비활성화
  autoflush=False,          # 자동 플러시 비활성화
  expire_on_commit=False,   # 커밋 시 만료 비활성화
)

# 실제 DB 의존성을 테스트 DB 의존성으로 대체
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_local() as session:
        yield session

# 앱의 의존성을 테스트용으로 교체
fastapi_app.dependency_overrides[get_db_session] = override_get_db

# 비동기 테스트 클라이언트를 위한 pytest fixture
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client