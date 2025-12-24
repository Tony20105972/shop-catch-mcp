"""
ShopCatch MCP - 중앙화된 설정 관리
성능 최적화 및 배포 환경 분리
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """환경변수 기반 설정 (타입 안전성 보장)"""
    
    # 서버 설정
    PORT: int = 10000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "production"  # development, staging, production
    
    # MCP 설정
    MCP_SERVER_NAME: str = "ShopCatch"
    MCP_TRANSPORT: str = "sse"
    
    # 네이버 API
    NAVER_CLIENT_ID: str
    NAVER_CLIENT_SECRET: str
    NAVER_API_TIMEOUT: float = 10.0
    NAVER_MAX_RESULTS: int = 5
    
    # 성능 튜닝
    HTTPX_MAX_CONNECTIONS: int = 100
    HTTPX_MAX_KEEPALIVE: int = 20
    
    # 로깅
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_FORMAT: str = "json"  # json or text
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """싱글톤 패턴으로 설정 객체 반환 (성능 최적화)"""
    return Settings()


# 전역 설정 객체
settings = get_settings()
