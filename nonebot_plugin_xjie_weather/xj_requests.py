import httpx


class xj_requests:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    async def xj_requests_main(self, place_url):
        try:
            response = await self.client.get(place_url)
            response.raise_for_status()
            print(response.status_code, "212")
            return response
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            # 直接抛出与延时相关的错误
            raise Exception(f"Connection or timeout error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
