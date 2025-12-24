"""
커스텀 예외 클래스
명확한 에러 핸들링 및 사용자 친화적 메시지
"""


class ShopCatchError(Exception):
    """기본 예외 클래스"""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_user_message(self) -> str:
        """사용자에게 보여줄 친화적 메시지"""
        return self.message


class NaverAPIError(ShopCatchError):
    """네이버 API 관련 에러"""
    
    def to_user_message(self) -> str:
        if self.details.get("status_code") == 429:
            return "⚠️ 네이버 API 사용량 한도에 도달했습니다. 잠시 후 다시 시도해주세요."
        elif self.details.get("status_code") == 401:
            return "🔒 네이버 API 인증에 실패했습니다. 관리자에게 문의해주세요."
        elif self.details.get("status_code") == 500:
            return "⚙️ 네이버 쇼핑 서비스가 일시적으로 불안정합니다. 잠시 후 다시 시도해주세요."
        return f"❌ 검색 중 오류가 발생했습니다: {self.message}"


class NetworkError(ShopCatchError):
    """네트워크 관련 에러"""
    
    def to_user_message(self) -> str:
        return "🌐 네트워크 연결에 문제가 있습니다. 인터넷 연결을 확인해주세요."


class ValidationError(ShopCatchError):
    """입력값 검증 에러"""
    
    def to_user_message(self) -> str:
        return f"⚠️ 입력값 오류: {self.message}"


class ConfigurationError(ShopCatchError):
    """설정 관련 에러"""
    
    def to_user_message(self) -> str:
        return "⚙️ 서버 설정에 문제가 있습니다. 관리자에게 문의해주세요."
