import os
import sys
import uvicorn

# 경로 설정
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from server.mcp_server import mcp

def main():
    # Render 환경 변수에서 포트 번호를 가져옵니다.
    port = int(os.environ.get("PORT", 10000))
    
    print("=" * 60)
    print(f"🚀 ShopCatch MCP Server - Fixed")
    print(f"📡 Binding to 0.0.0.0:{port}")
    print("=" * 60)

    # ✅ 해결 방법: FastMCP는 .app 속성 대신 .get_asgi_app() 메서드를 제공합니다.
    # 이 메서드가 uvicorn이 실행할 수 있는 Starlette/ASGI 객체를 반환합니다.
    app = mcp.get_asgi_app()

    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=port, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
