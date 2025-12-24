import os
import sys
import uvicorn

# 경로 설정
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from server.mcp_server import mcp

def main():
    port = int(os.environ.get("PORT", 10000))
    
    print("=" * 60)
    print(f"🚀 ShopCatch MCP Server - Final Fix")
    print(f"📡 Binding to 0.0.0.0:{port}")
    print("=" * 60)

    # ✅ mcp.app은 Starlette/FastAPI 앱 객체입니다.
    # uvicorn은 이 'app' 객체를 실행해야 합니다.
    uvicorn.run(
        mcp.app,  # mcp 자체가 아니라 mcp.app을 전달
        host="0.0.0.0", 
        port=port, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
