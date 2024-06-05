import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class xj_requests:
    def __init__(self):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,  # 延迟时间
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        pass

    def xj_requests_main(self, place_url):
        try:
            response = self.session.get(place_url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as err:
            if isinstance(err, requests.exceptions.Timeout):
                print("Request timed out.")
                return None
            elif isinstance(err, requests.exceptions.ConnectionError):
                print("Connection error occurred.")
                return None
            elif isinstance(err, requests.exceptions.HTTPError):
                print(f"HTTP error occurred: {err}")
                return None
            else:
                print(f"Other error occurred: {err}")
                return None
