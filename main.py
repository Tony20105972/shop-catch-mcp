"""
ShopCatch MCP 서버 진입점
최종 안정화 버전: 인자 없는 mcp.run() 사용
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
        logger.info(f"🚀 자동 설정 모드로 서버를 시작합니다.")
        logger.info("=" * 60)
        
        # ✅ 최종 해결책: 인자를 비우고 호출합니다.
        # 이렇게 하면 FastMCP 내부의 자동 감지 로직이 
        # 환경 변수 PORT를 찾아 0.0.0.0:10000으로 서버를 띄웁니다.
        mcp.run()
    
    except Exception as e:
        logger.error(f"❌ 서버 시작 실패: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
