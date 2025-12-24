import os
import sys
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

# 경로 설정
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from server.mcp_server import mcp

# 1. FastMCP 객체가 가지고 있는 실제 ASGI 앱(서버 엔진)을 직접 꺼냅니다.
# .run() 대신 이 객체를 직접 사용하면 uvicorn으로 우리가 직접 포트를 제어할 수 있습니다.
# 만약 mcp.app이 없으면 mcp._app 등으로 시도합니다.
mcp_app = getattr(mcp, "app", getattr(mcp, "_app", None))

if mcp_app is None:
    # 최후의 수단: mcp 객체 자체가 ASGI 앱 역할을 하는 경우
    mcp_app = mcp

def main():
    port = int(os.environ.get("PORT", 10000))
    
    print("=" * 60)
    print(f"🚀 ShopCatch MCP Server - Direct Uvicorn Mode")
    print(f"📡 Binding to 0.0.0.0:{port}")
    print("=" * 60)

    # 2. mcp.run()을 절대 쓰지 않고 uvicorn으로 강제 기동합니다.
    uvicorn.run(
        mcp_app, 
        host="0.0.0.0", 
        port=port, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
