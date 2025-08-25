# __init__.py
# DB 모듈 초기화 파일

# 패키지 호출
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 환경변수 호출
from core.db_config import settings

# DB 연결 정보
DB_URL = settings.DB_URL

# 외부에서 DB모듈 호출 시 설정
__all__ = ['engine', 'get_db_session', 'async_session']

# DB 엔진 생성
engine = create_async_engine(DB_URL, echo=True)

# 세션 생성기
async_session = sessionmaker(autocommit=False, 
                             autoflush=False, 
                             bind=engine, 
                             class_=AsyncSession)

# DB 세션 생성
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session