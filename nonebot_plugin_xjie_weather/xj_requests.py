import httpx
from typing import Dict, Any


class xj_requests:
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def xj_requests_main(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        """
        异步地向提供的URL发送GET请求。

        参数
        ----
        url : str
            发送GET请求的目标URL。
        params : Dict[str, Any], 可选
            请求中包含的查询参数，默认为None。
        headers : Dict[str, str], 可选
            请求中包含的头信息，默认为None。

        返回
        ----
        httpx.Response
            如果请求成功，则返回服务器的响应，否则返回None。

        异常
        ----
        httpx.HTTPStatusError
            如果HTTP状态码表示错误。
        httpx.ConnectError
            如果发生连接错误。
        httpx.ReadTimeout
            如果在等待数据时请求超时。
        Exception
            对于任何其他未预期的错误。
        """
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            print(response.status_code, "请求成功")
            return response
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误发生: {e}")
            return None
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            print(f"连接或超时错误: {e}")
            return None
        except Exception as e:
            print(f"发生了未预期的错误: {e}")
            return None
