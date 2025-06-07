import logging

import httpx


async def fetch_from_api(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logging.error(f'HTTP error for {url}: {e}')
        raise
