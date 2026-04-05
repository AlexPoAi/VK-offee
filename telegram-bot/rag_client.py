"""
RAG Client для VK-offee Telegram Bot
Подключается к RAG API и возвращает ответы на вопросы по базе знаний.
Retry x3 при недоступности API.
"""

import os
import logging
import requests
from typing import Optional, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Localhost остаётся удобным dev fallback, но production/cloud runtime
# обязан задавать RAG_API_URL явно через env.
RAG_API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000")
RAG_TIMEOUT = int(os.getenv("RAG_TIMEOUT", "30"))


class RAGClient:
    """Клиент для взаимодействия с VK-offee RAG API"""

    def __init__(self, base_url: str = RAG_API_URL, timeout: int = RAG_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def is_available(self) -> bool:
        """Проверяет доступность RAG API"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            data = response.json()
            return response.status_code == 200 and data.get("status") == "healthy"
        except Exception:
            return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        reraise=True,
    )
    def _call_query(self, question: str, n_results: int = 5) -> Dict:
        """Внутренний вызов RAG API с retry x3"""
        response = requests.post(
            f"{self.base_url}/query",
            json={"question": question, "n_results": n_results},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def query(self, question: str, n_results: int = 5) -> Optional[Dict]:
        """
        Запрос к RAG. Возвращает dict с answer и sources, или None при ошибке.
        """
        try:
            result = self._call_query(question, n_results)
            logger.info(f"RAG ответил на вопрос ({len(result.get('sources', []))} источников)")
            return result
        except requests.ConnectionError:
            logger.error("RAG API недоступен (ConnectionError) после 3 попыток")
            return None
        except requests.Timeout:
            logger.error("RAG API не ответил за %ds после 3 попыток", self.timeout)
            return None
        except requests.HTTPError as e:
            logger.error("RAG API вернул ошибку: %s", e)
            return None
        except Exception as e:
            logger.error("Неожиданная ошибка RAG: %s", e)
            return None

    def format_answer(self, result: Dict, show_sources: bool = True) -> str:
        """Форматирует ответ RAG для Telegram"""
        answer = result.get("answer", "Нет ответа")
        sources = result.get("sources", [])

        text = answer

        if show_sources and sources:
            # Уникальные Pack-источники
            packs = list(dict.fromkeys(
                s.get("pack", "?") for s in sources if s.get("pack")
            ))
            if packs:
                packs_str = ", ".join(packs)
                text += f"\n\n📚 _Источники: {packs_str}_"

        return text


# Глобальный singleton
_rag_client: Optional[RAGClient] = None


def get_rag_client() -> RAGClient:
    """Возвращает singleton RAGClient"""
    global _rag_client
    if _rag_client is None:
        _rag_client = RAGClient()
    return _rag_client
