import httpx
from typing import Dict, Any


class xj_requests:
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def xj_requests_main(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            print(response.status_code, "请求成功")
            return response
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            print(f"Connection or timeout error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
