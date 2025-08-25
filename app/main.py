# 패키지 호출
from fastapi import Depends, FastAPI
from fastapi import HTTPException, status
import logging
from logging.config import dictConfig

# DB 패키지에서 의존성 함수 호출
from DB import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# 로깅 환경 설정 호출
from core.logging_config import LOGGING_CONFIG

# FastAPI 인스턴스 생성
app = FastAPI()

# 로깅 설정
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")   # 'app'이라는 이름으로 설정된 로그 호출

# 애플리케이션 수명 주기 관리
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check(db: AsyncSession = Depends(get_db_session)):
    '''
    Health check endpoint
    DB에 간단한 쿼리를 실행하여 DB 연결 상태를 확인
    '''
    # 통신 상태 확인
    try:
        result = await db.execute(text("SELECT 1"))  # 간단한 쿼리 실행
        
        # result의 값이 1이 아닌 경우는 비정상으로 간주
        if result.scalar_one_or_none() != 1:
            logger.error("Health check failed: DataBase query returned an unexpected value.")
            
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database is not responding correctly value:{result.scalar_one_or_none()}"
            )
            
        # 데이터베이스 연결 성공
        logger.info("Database connection successful")
        return {'status': 'ok',
                'database': 'healthy'}
    
    # 데이터베이스 연결 실패
    except Exception as e:
        # 503 Service Unavailable 반환
        logger.error(f"Health check failed: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed {e}"
        )

# GET 요청 처리
@app.get("/")
def read_root():
    # 루트 엔드포인트 연결
    try:
        logger.info('Root endpoint accessed')       # 루트 엔드포인트 접근
        return {"message": "success connection"}    # 루트 엔드포인트 응답
    # 루트 엔드포인트 예외 처리
    except Exception as e:
        logger.error(f"Error accessing root endpoint: {e}")         # 루트 엔드포인트 예외 처리
        return {"message": "failed connection", "error": str(e)}    # 루트 엔드포인트 예외 응답
