"""
ShopCatch MCP 서버 진입점
Application Exited Early 해결 버전
"""
import sys
import os
import asyncio

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
        logger.info(f"🚀 Render 배포 모드 (SSE)")
        logger.info("=" * 60)
        
        # ✅ 해결책: transport를 명시하고, 비동기적으로 실행이 유지되도록 합니다.
        # FastMCP의 run 메서드는 transport="sse"가 주어지면 내부적으로 서버 엔진을 가동합니다.
        mcp.run(transport="sse")
    
    except Exception as e:
        logger.error(f"❌ 서버 가동 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
