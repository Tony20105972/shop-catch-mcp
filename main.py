"""
ShopCatch MCP 서버 진입점
FastAPI를 사용하지 않는 Pure MCP 구현으로 ASGI 충돌 완전 제거
"""
import sys
import asyncio
from config import settings
from utils.logger import logger
from server.mcp_server import mcp


def validate_environment():
    """환경 변수 검증"""
    required_vars = ["NAVER_CLIENT_ID", "NAVER_CLIENT_SECRET"]
    missing_vars = []
    
    for var in required_vars:
        if not getattr(settings, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ 필수 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        logger.error("💡 .env 파일을 확인하거나 Render 환경 변수를 설정해주세요.")
        sys.exit(1)


def main():
    """메인 함수"""
    try:
        # 환경 변수 검증
        validate_environment()
        
        # 서버 정보 출력
        logger.info("=" * 60)
        logger.info(f"🏪 {settings.MCP_SERVER_NAME} MCP Server")
        logger.info("=" * 60)
        logger.info(f"📍 Host: {settings.HOST}:{settings.PORT}")
        logger.info(f"🔧 Environment: {settings.ENVIRONMENT}")
        logger.info(f"🚀 Transport: {settings.MCP_TRANSPORT}")
        logger.info(f"📊 Log Level: {settings.LOG_LEVEL}")
        logger.info("=" * 60)
        
        # Pure MCP 서버 실행 (FastAPI 없음)
        # 이 방식이 SSE 충돌을 완전히 방지합니다
        mcp.run(
            transport=settings.MCP_TRANSPORT,
            host=settings.HOST,
            port=settings.PORT
        )
    
    except KeyboardInterrupt:
        logger.info("\n⚠️ 사용자에 의해 서버가 중단되었습니다.")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"❌ 서버 시작 실패: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
