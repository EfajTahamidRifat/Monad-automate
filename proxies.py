import requests
import concurrent.futures
import random
import time


class ProxyTester:
    def __init__(self,
                 proxy_url='https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json'):
        """[removed long docstring]"""
        Fetch proxies from the specified URL

        :return: List of proxy dictionaries
        """[removed long docstring]"""
        Test a single proxy for connectivity and speed

        :param proxy_data: Dictionary containing proxy information
        :param timeout: Connection timeout in seconds
        :return: Tuple of (is_working, proxy_dict, response_time)
        """[removed long docstring]"""
        Concurrently test proxies

        :param max_workers: Maximum number of concurrent proxy tests
        :param max_proxies: Maximum number of proxies to test
        :return: List of working proxies
        """[removed long docstring]"""
        Make a GET request using a working proxy

        :param url: URL to request
        :param proxy_index: Index of the proxy to use from working_proxies
        :return: Response text or None
        """
        if not self.working_proxies:
            print("No working proxies available")
            return None

        try:
            proxy = self.working_proxies[proxy_index]['proxy']
            response = requests.get(url, proxies=proxy, timeout=10)
            return response.text
        except Exception as e:
            print(f"Request failed with proxy {proxy}: {e}")
            return None


def get_free_proxy():
    # Create a ProxyTester instance
    proxy_tester = ProxyTester()

    # Fetch proxies
    proxy_tester.fetch_proxies()

    # Test proxies
    print("Testing for working proxies...")
    proxy_tester.test_proxies(max_workers=20, max_proxies=50)

    # Example: Make a request using a proxy
    proxy_index = -1  # index starts at zero so set to -1
    if proxy_tester.working_proxies:
        for working_proxy in proxy_tester.working_proxies:
            proxy_index += 1
            response = proxy_tester.make_request('http://httpbin.org/ip', proxy_index)
            if response:
                # print("Successful request response:", response)
                return working_proxy
