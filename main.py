"""
ShopCatch MCP 서버 진입점
Render 포트 바인딩 및 외부 접속(0.0.0.0) 해결 버전
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
        
        # Render 환경 변수에서 포트를 가져오고, 기본값으로 10000을 설정합니다.
        port_env = int(os.environ.get("PORT", 10000))
        
        logger.info("=" * 60)
        logger.info(f"🏪 {settings.MCP_SERVER_NAME} MCP Server Starting...")
        logger.info(f"🚀 Binding to 0.0.0.0:{port_env} (Render Mode)")
        logger.info("=" * 60)
        
        # ✅ 핵심 수정: host="0.0.0.0"으로 설정하여 외부 접속을 허용합니다.
        # port를 Render가 요구하는 포트(10000)로 일치시킵니다.
        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=port_env
        )
    
    except Exception as e:
        logger.error(f"❌ 서버 가동 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
