# core/db_config.py
# 데이터베이스 환경 변수 설정

# 패기지 호출
from pydantic_settings import BaseSettings, SettingsConfigDict

# 데이터베이스 환경 변수 설정
class Settings(BaseSettings):
    # 데이터베이스 URL
    DB_URL: str

    # 데이터베이스 연결 URL
    model_config = SettingsConfigDict(
        env_file = ".env/.env",         # 환경 변수 파일 경로
        env_file_encoding = "utf-8"     # 환경 변수 파일 인코딩
    )

# 설정 객체를 생성하여 다른 모듈에서 사용할 수 있도록 함
settings = Settings()
