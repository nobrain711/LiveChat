# 패키지 호출
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

# DB 폴더 호출
from DB import get_db_session

# FastAPI 인스턴스 생성
app = FastAPI()

# GET 요청 처리
@app.get("/")
def read_root():
    try:
        return {"message": "success connection"}
    except Exception as e:
        return {"message": "failed connection", "error": str(e)}

# DB 연결 테스트
@app.get("/db-test")
async def db_test(session: AsyncSession = Depends(get_db_session)):
    try:
        return {"message": "DB connection successful"}
    except Exception as e:
        return {"message": "DB connection failed", "error": str(e)}