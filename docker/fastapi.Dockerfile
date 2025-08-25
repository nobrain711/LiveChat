# 기본 이미지 설정
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# OS 패키지 및 시간대 설정
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev build-essential curl tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Rust 설치 (비대화식)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app .

# 포트 노출
EXPOSE 8000