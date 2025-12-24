"""
ShopCatch MCP 서버 진입점
디버깅 정보 강화 버전
"""
import sys
import os

# 디버깅: 현재 작업 디렉토리와 Python 경로 출력
print(f"🔍 Current Working Directory: {os.getcwd()}")
print(f"🔍 Python Path: {sys.path}")
print(f"🔍 Script Location: {os.path.abspath(__file__)}")
print(f"🔍 Directory Contents: {os.listdir('.')}")

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
print(f"✅ Added to path: {project_root}")

# 디렉토리 존재 확인
required_dirs = ['server', 'services', 'utils']
for dir_name in required_dirs:
    dir_path = os.path.join(project_root, dir_name)
    exists = os.path.exists(dir_path)
    has_init = os.path.exists(os.path.join(dir_path, '__init__.py'))
    print(f"📁 {dir_name}: exists={exists}, has_init={has_init}")

try:
    print("\n🔄 Importing modules...")
    from config import settings
    print("✅ config imported")
    
    from utils.logger import logger
    print("✅ logger imported")
    
    from server.mcp_server import mcp
    print("✅ mcp_server imported")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"❌ Error details: {e.__class__.__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


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
        
        # Pure MCP 서버 실행
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
