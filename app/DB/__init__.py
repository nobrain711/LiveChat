# 패키지 호출
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# DB 연결 정보
DB_URL = os.getenv("DB_URL", "postgresql+asyncpg://chat:dev2025@db:5432/chat")

# DB 엔진 생성
engine = create_async_engine(DB_URL, echo=True)

# 세션 생성기
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# DB 세션 생성
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session