"""
LLM 친화적 데이터 포매터
토큰 효율성과 가독성을 동시에 최적화
"""
from typing import List, Dict, Any
import re


def clean_html(text: str) -> str:
    """HTML 태그 제거 (네이버 API는 <b> 태그를 포함함)"""
    return re.sub(r'<[^>]+>', '', text)


def format_price(price: str) -> str:
    """가격 포맷팅 (천 단위 구분)"""
    try:
        return f"{int(price):,}원"
    except (ValueError, TypeError):
        return f"{price}원"


def format_shopping_results(items: List[Dict[str, Any]], keyword: str) -> str:
    """
    네이버 쇼핑 검색 결과를 LLM이 이해하기 쉬운 형식으로 변환
    
    성능 최적화:
    - 불필요한 필드 제거
    - 토큰 수 최소화
    - 시각적 구분자 활용
    """
    if not items:
        return f"'{keyword}'에 대한 검색 결과가 없습니다. 다른 키워드로 검색해보세요."
    
    result_lines = [
        f"🔍 '{keyword}' 검색 결과 (총 {len(items)}개)\n",
        "─" * 60
    ]
    
    for idx, item in enumerate(items, 1):
        title = clean_html(item.get('title', '제목 없음'))
        price = format_price(item.get('lprice', '0'))
        link = item.get('link', '')
        brand = item.get('brand', '').strip()
        mall_name = item.get('mallName', '').strip()
        
        # 간결하면서도 정보량이 풍부한 포맷
        product_info = [
            f"\n📦 {idx}. {title}",
            f"   💰 최저가: {price}"
        ]
        
        # 선택적 정보 추가 (있을 때만)
        if brand:
            product_info.append(f"   🏷️  브랜드: {brand}")
        if mall_name:
            product_info.append(f"   🏬 판매처: {mall_name}")
        
        product_info.append(f"   🔗 구매링크: {link}")
        
        result_lines.extend(product_info)
    
    result_lines.append("\n" + "─" * 60)
    result_lines.append("💡 가격은 실시간으로 변동될 수 있습니다.")
    
    return "\n".join(result_lines)


def format_error_message(error_type: str, details: str = "") -> str:
    """에러 메시지 포맷팅 (사용자 친화적)"""
    error_templates = {
        "api_error": "❌ 네이버 쇼핑 API 오류가 발생했습니다.",
        "network_error": "🌐 네트워크 연결 오류가 발생했습니다.",
        "timeout": "⏱️ 응답 시간이 초과되었습니다. 다시 시도해주세요.",
        "no_results": "🔍 검색 결과가 없습니다.",
        "invalid_keyword": "⚠️ 검색어를 확인해주세요."
    }
    
    base_message = error_templates.get(error_type, "❌ 알 수 없는 오류가 발생했습니다.")
    
    if details:
        return f"{base_message}\n상세 정보: {details}"
    return base_message


def format_health_status(status: Dict[str, Any]) -> str:
    """헬스체크 결과 포맷팅"""
    emoji = "✅" if status.get("healthy") else "❌"
    return f"{emoji} 서버 상태: {status.get('status', 'unknown')}"
