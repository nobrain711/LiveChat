# logging_config.py
# 로그 관련 환경변수 설정

# 패키지 호출
import logging.config
import os

# 환경변수에서 로그 파일 경로를 가져오거나 기본값을 사용
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log.json")

# 로그 파일이 위치할 디렉토리 경로 취득
LOG_FILE_DIR = os.path.dirname(LOG_FILE_PATH)

# 로그 폴더가 위치하지 않으면 로그 폴더를 생성
if not os.path.exists(LOG_FILE_DIR):
    os.makedirs(LOG_FILE_DIR)

# 로그 설정
LOGGING_CONFIG = {
  'version': 1, # 작성 버전
  'disable_existing_loggers': False,  # 기존 로거 비활성화
  # 포맷 설정
  'formatters' : {
    # 기본 포맷 설정
    'default': {
      'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s', # 기본 포맷 ex) 2023-01-01 12:00:00 - app - INFO - 메시지
      'datefmt': '%Y-%m-%d %H:%M:%S',                                   # 날짜 포맷
    },
    # json 포맷 설정
    'json' : {
      '()' : 'pythonjsonlogger.jsonlogger.JsonFormatter',               # json 포맷터
      'format' : '%(asctime)s - %(name)s - %(levelname)s - %(message)s' # json 포맷 ex) {"time": "2023-01-01 12:00:00", "name": "app", "level": "INFO", "message": "메시지"}
    }
  },
  # 핸들러 설정
  'handlers' : {
    # 콘솔 핸들러 설정
    'console': {
      'class': 'logging.StreamHandler', # 콘솔 출력 핸들러
      'level': 'INFO',                  # 로그 레벨 설정: INFO
      'formatter': 'default',           # 포맷 설정: 기본 포맷
      'stream': 'ext://sys.stdout'      # 출력 스트림 설정: 표준 출력
    },
    # 파일 핸들러 설정
    'file': {
      'class': 'logging.handlers.RotatingFileHandler',  # 파일 핸들러
      'level': 'INFO',                                  # 로그 레벨 설정: INFO
      'formatter': 'json',                              # 포맷 설정: json 포맷
      'filename': LOG_FILE_PATH,                        # 파일 이름 설정: logs/app.log.json
      'maxBytes': 1024 * 1024 * 10,                     # 최대 파일 크기 설정: 10 MB
      'backupCount': 3,                                 # 백업 파일 개수 설정: 3
      'encoding': 'utf-8',                              # 파일 인코딩 설정: UTF-8
    },
  },
  # 로그 설정
  'loggers': {
    # app 로그 설정
    'app':{
     'handlers': ['console', 'file'], # 핸들러 설정
     'level': 'INFO',                 # 로그 레벨 설정: INFO
     'propagate': False               # 전파 설정: False
    },
    # uvicorn.access 로그 설정
    'uvicorn.access': {
      'handlers': ['console'],        # 핸들러 설정: 콘솔
      'level': 'INFO',                # 로그 레벨 설정: INFO
      'propagate': False              # 전파 설정: False
    },
    # SQL 로그 설정
    'sqlalchemy.engine': {
      'handlers': ['console'],        # 핸들러 설정: 콘솔
      'level': 'INFO',                # 로그 레벨 설정: INFO
      'propagate': False              # 전파 설정: False
    },
  },
  # 루트 로그 설정
  'root': {
    'handlers': ['console'],          # 핸들러 설정: 콘솔
    'level': 'INFO'                   # 로그 레벨 설정: INFO
  }
}