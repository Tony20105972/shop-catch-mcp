"""
ShopCatch MCP 서버 및 툴 정의
FastMCP를 이용한 Pure MCP 구현
"""
import time
from mcp.server.fastmcp import FastMCP
from config import settings
from utils.logger import logger, log_tool_execution
from utils.exceptions import ShopCatchError
from services.naver_api import search_shopping
from services.formatter import format_shopping_results, format_error_message


# MCP 서버 인스턴스 생성
mcp = FastMCP(settings.MCP_SERVER_NAME)


@mcp.tool()
async def search_naver_shopping(
    keyword: str,
    sort: str = "sim"
) -> str:
    """
    네이버 쇼핑에서 상품을 검색합니다.
    
    Args:
        keyword: 검색할 상품명 또는 키워드 (예: "무선 이어폰", "노트북")
        sort: 정렬 방식
            - "sim": 정확도순 (기본값, 추천)
            - "asc": 가격 낮은 순
            - "dsc": 가격 높은 순
            - "date": 최신순
    
    Returns:
        검색 결과를 읽기 쉬운 형식으로 반환합니다.
        가격, 브랜드, 판매처, 구매 링크 등의 정보를 포함합니다.
    
    Examples:
        - "무선 이어폰 검색해줘" → search_naver_shopping(keyword="무선 이어폰")
        - "노트북을 가격 낮은 순으로 찾아줘" → search_naver_shopping(keyword="노트북", sort="asc")
    
    Tips:
        - 검색 결과가 없으면 키워드를 바꿔보세요
        - 가격은 실시간으로 변동될 수 있습니다
    """
    start_time = time.time()
    success = False
    
    try:
        logger.info(f"툴 실행: search_naver_shopping(keyword={keyword}, sort={sort})")
        
        # 네이버 API 호출
        items = await search_shopping(keyword, sort=sort)
        
        # 결과 포맷팅
        result = format_shopping_results(items, keyword)
        
        success = True
        return result
    
    except ShopCatchError as e:
        # 예상된 에러 (사용자 친화적 메시지)
        logger.warning(f"툴 실행 실패: {e.message}", extra=e.details)
        return e.to_user_message()
    
    except Exception as e:
        # 예상치 못한 에러
        logger.error(f"툴 실행 중 예외 발생: {e}", exc_info=True)
        return format_error_message("api_error", str(e))
    
    finally:
        # 실행 시간 로깅 (성능 모니터링)
        duration = time.time() - start_time
        log_tool_execution(
            tool_name="search_naver_shopping",
            params={"keyword": keyword, "sort": sort},
            success=success,
            duration=duration
        )


@mcp.tool()
async def get_lowest_price(keyword: str) -> str:
    """
    특정 상품의 최저가를 빠르게 찾습니다.
    
    이 툴은 search_naver_shopping의 특화 버전으로,
    자동으로 가격 낮은 순으로 정렬하여 최저가를 보여줍니다.
    
    Args:
        keyword: 검색할 상품명 (예: "아이폰 15 Pro", "다이슨 청소기")
    
    Returns:
        가격 낮은 순으로 정렬된 상품 목록
    
    Examples:
        - "아이폰 15 최저가 알려줘" → get_lowest_price(keyword="아이폰 15")
    """
    start_time = time.time()
    success = False
    
    try:
        logger.info(f"툴 실행: get_lowest_price(keyword={keyword})")
        
        # 가격 낮은 순으로 검색
        items = await search_shopping(keyword, sort="asc")
        
        # 결과 포맷팅 (최저가 강조)
        if not items:
            return f"'{keyword}'에 대한 검색 결과가 없습니다."
        
        result = format_shopping_results(items, keyword)
        result += "\n\n💡 가격 낮은 순으로 정렬되었습니다."
        
        success = True
        return result
    
    except ShopCatchError as e:
        logger.warning(f"툴 실행 실패: {e.message}", extra=e.details)
        return e.to_user_message()
    
    except Exception as e:
        logger.error(f"툴 실행 중 예외 발생: {e}", exc_info=True)
        return format_error_message("api_error", str(e))
    
    finally:
        duration = time.time() - start_time
        log_tool_execution(
            tool_name="get_lowest_price",
            params={"keyword": keyword},
            success=success,
            duration=duration
        )


# 서버 라이프사이클 이벤트
#@mcp.on_startup()
#async def startup():
    #"""서버 시작 시 실행"""
    #logger.info(f"🚀 {settings.MCP_SERVER_NAME} 서버 시작")
    #logger.info(f"환경: {settings.ENVIRONMENT}")
    #logger.info(f"포트: {settings.PORT}")
    #logger.info(f"로그 레벨: {settings.LOG_LEVEL}")


#@mcp.on_shutdown()
#async def shutdown():
    #"""서버 종료 시 실행 (리소스 정리)"""
    #logger.info("🛑 서버 종료 중...")
    
    # HTTP 클라이언트 정리
   # from services.naver_api import get_naver_client
    #try:
        #client = get_naver_client()
       # await client.close()
        #logger.info("✅ 네이버 API 클라이언트 정리 완료")
    #except Exception as e:
        #logger.error(f"클라이언트 정리 중 오류: {e}")
    
    #logger.info("👋 서버 종료 완료")
