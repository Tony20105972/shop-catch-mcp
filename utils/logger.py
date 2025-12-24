"""
구조화된 로깅 시스템
Render 대시보드에서 보기 좋은 로그 출력
"""
import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from config import settings


class StructuredFormatter(logging.Formatter):
    """JSON 형식의 구조화된 로그 포매터"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # 추가 컨텍스트 정보
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # 예외 정보
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """사람이 읽기 좋은 텍스트 포매터"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return f"{color}[{timestamp}] {record.levelname:8}{reset} | {record.name:20} | {record.getMessage()}"


def setup_logger(name: str = "shopcatch") -> logging.Logger:
    """로거 설정 및 반환"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 핸들러 중복 방지
    if logger.handlers:
        return logger
    
    # 콘솔 핸들러
    handler = logging.StreamHandler(sys.stdout)
    
    # 포맷 선택
    if settings.LOG_FORMAT == "json":
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(TextFormatter())
    
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger


# 전역 로거
logger = setup_logger()


def log_tool_execution(tool_name: str, params: Dict[str, Any], success: bool, duration: float):
    """툴 실행 로그 (성능 모니터링용)"""
    logger.info(
        f"Tool executed: {tool_name}",
        extra={
            "tool": tool_name,
            "params": params,
            "success": success,
            "duration_ms": round(duration * 1000, 2)
        }
    )
