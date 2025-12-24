"""
ShopCatch MCP 서버 진입점
TypeError (host 인자 에러) 해결 버전
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from config import settings
    from utils.logger import logger
    from server.mcp_server import mcp
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def validate_environment():
    """환경 변수 검증"""
    required_vars = ["NAVER_CLIENT_ID", "NAVER_CLIENT_SECRET"]
    for var in required_vars:
        if not getattr(settings, var, None):
            logger.error(f"❌ 필수 환경 변수 누락: {var}")
            sys.exit(1)

def main():
    """메인 함수"""
    try:
        validate_environment()
        
        logger.info("=" * 60)
        logger.info(f"🏪 {settings.MCP_SERVER_NAME} MCP Server Starting...")
        logger.info(f"🚀 Transport: {settings.MCP_TRANSPORT} | Port: {settings.PORT}")
        logger.info("=" * 60)
        
        # ✅ 핵심 수정: host 인자를 제거하고 port만 전달합니다.
        # FastMCP 내부적으로 uvicorn을 실행하며 기본적으로 0.0.0.0에 바인딩됩니다.
        mcp.run(
            transport=settings.MCP_TRANSPORT,
            port=settings.PORT
        )
    
    except Exception as e:
        logger.error(f"❌ 서버 시작 실패: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
