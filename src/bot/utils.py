from datetime import datetime
import logging

import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def fetch_from_api(url: str) -> dict:
    """
    Выполнить GET-запрос к API и возвратить результат в JSON.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logging.error(f'HTTP error for {url}: {e}')
        raise


def format_post_date(dt_string: str) -> str:
    """
    Преобразовать строку с датой из ISO-формата (например, '2024-06-08T18:04:25.514104')
    в формат 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return dt_string.replace('T', ' ').split('.')[0]
