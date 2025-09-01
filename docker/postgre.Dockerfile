# Dockerfile for PostgreSQL
# postgres의 공식 이미지를 기반으로 합니다.
# PostgreSQL 15 버전을 사용합니다.
FROM postgres:15

# RUN으로 OS 업데이트 및 한국어 관련 로케일 생성 후 임시 파일 제거
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y locales && \
    sed -i -e 's/# ko_KR.UTF-8 UTF-8/ko_KR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# PostgreSQL container의 기본 언어 설정
ENV LANG=ko_KR.utf8
ENV LC_ALL=ko_KR.utf8