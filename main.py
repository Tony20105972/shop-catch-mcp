"""
ShopCatch MCP 서버 - Starlette 마운트 구조
가장 안정적인 Render 배포용 진입점
"""
import uvicorn
import os
import sys
from starlette.applications import Starlette
from starlette.routing import Mount

# 프로젝트 루트 경로 설정
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

# 1. FastMCP 객체를 Starlette 앱에 연결합니다.
# FastMCP는 내부적으로 Starlette 앱(mcp.app)을 가지고 있습니다.
app = Starlette(
    routes=[
        Mount("/", mcp.app)  # 모든 MCP 요청을 mcp.app으로 전달
    ]
)

def main():
    """메인 실행 함수"""
    try:
        validate_environment()
        
        # Render에서 제공하는 포트 확인 (기본값 10000)
        port = int(os.environ.get("PORT", 10000))
        
        logger.info("=" * 60)
        logger.info(f"🏪 {settings.MCP_SERVER_NAME} starting via Starlette")
        logger.info(f"🚀 Running on 0.0.0.0:{port}")
        logger.info("=" * 60)
        
        # 2. uvicorn을 직접 실행하여 0.0.0.0과 포트를 강제 지정합니다.
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"❌ 서버 가동 실패: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
