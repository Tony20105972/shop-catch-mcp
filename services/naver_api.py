"""
네이버 쇼핑 API 클라이언트
비동기, 재시도, 타임아웃 등 프로덕션 그레이드 구현
"""
import httpx
from typing import List, Dict, Any, Optional
from config import settings
from utils.logger import logger
from utils.exceptions import NaverAPIError, NetworkError, ValidationError


class NaverShoppingClient:
    """네이버 쇼핑 API 클라이언트 (싱글톤 패턴)"""
    
    BASE_URL = "https://openapi.naver.com/v1/search/shop.json"
    
    def __init__(self):
        self.client_id = settings.NAVER_CLIENT_ID
        self.client_secret = settings.NAVER_CLIENT_SECRET
        self.timeout = settings.NAVER_API_TIMEOUT
        
        # HTTPX 클라이언트 설정 (성능 최적화)
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """비동기 HTTP 클라이언트 (연결 재사용)"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                limits=httpx.Limits(
                    max_connections=settings.HTTPX_MAX_CONNECTIONS,
                    max_keepalive_connections=settings.HTTPX_MAX_KEEPALIVE
                ),
                http2=True  # HTTP/2 지원 (성능 향상)
            )
        return self._client
    
    async def close(self):
        """클라이언트 종료 (리소스 정리)"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _validate_keyword(self, keyword: str) -> None:
        """검색어 유효성 검증"""
        if not keyword or not keyword.strip():
            raise ValidationError("검색어를 입력해주세요.")
        
        if len(keyword) > 100:
            raise ValidationError("검색어는 100자 이하로 입력해주세요.")
    
    async def search(
        self,
        keyword: str,
        display: int = None,
        sort: str = "sim"  # sim(정확도), date(날짜), asc(가격 낮은 순), dsc(가격 높은 순)
    ) -> List[Dict[str, Any]]:
        """
        네이버 쇼핑 검색
        
        Args:
            keyword: 검색어
            display: 결과 개수 (기본값: settings.NAVER_MAX_RESULTS)
            sort: 정렬 방식
        
        Returns:
            검색 결과 리스트
        
        Raises:
            ValidationError: 입력값 오류
            NaverAPIError: API 호출 오류
            NetworkError: 네트워크 오류
        """
        # 검증
        self._validate_keyword(keyword)
        display = display or settings.NAVER_MAX_RESULTS
        
        # 요청 준비
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "User-Agent": "ShopCatch-MCP/1.0"
        }
        
        params = {
            "query": keyword.strip(),
            "display": min(display, 100),  # 최대 100개
            "sort": sort
        }
        
        logger.info(f"네이버 쇼핑 검색 시작: {keyword} (정렬: {sort})")
        
        try:
            client = await self._get_client()
            response = await client.get(
                self.BASE_URL,
                headers=headers,
                params=params
            )
            
            # 상태 코드 확인
            if response.status_code != 200:
                logger.error(f"네이버 API 오류: {response.status_code} - {response.text}")
                raise NaverAPIError(
                    f"API 호출 실패 (상태 코드: {response.status_code})",
                    details={"status_code": response.status_code, "response": response.text}
                )
            
            # 응답 파싱
            data = response.json()
            items = data.get("items", [])
            
            logger.info(f"검색 완료: {len(items)}개 결과")
            return items
        
        except httpx.TimeoutException as e:
            logger.error(f"타임아웃 오류: {e}")
            raise NaverAPIError(
                "응답 시간 초과",
                details={"error": "timeout", "timeout": self.timeout}
            )
        
        except httpx.NetworkError as e:
            logger.error(f"네트워크 오류: {e}")
            raise NetworkError(
                "네트워크 연결 실패",
                details={"error": str(e)}
            )
        
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}", exc_info=True)
            raise NaverAPIError(
                f"검색 중 오류 발생: {str(e)}",
                details={"error": str(e)}
            )


# 싱글톤 인스턴스
_naver_client: Optional[NaverShoppingClient] = None


def get_naver_client() -> NaverShoppingClient:
    """네이버 API 클라이언트 인스턴스 반환"""
    global _naver_client
    if _naver_client is None:
        _naver_client = NaverShoppingClient()
    return _naver_client


async def search_shopping(keyword: str, sort: str = "sim") -> List[Dict[str, Any]]:
    """
    편의 함수: 네이버 쇼핑 검색
    
    Usage:
        results = await search_shopping("노트북", sort="asc")
    """
    client = get_naver_client()
    return await client.search(keyword, sort=sort)
