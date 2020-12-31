from typing import Dict, Tuple, Union

import time
import requests
import random

from .base_parser import BaseEndpointParser

_DEFAULT_BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/javascript, */*; q=0.01",
}
_DEFAULT_FIRST_PAGE_NUM = 1
_VALID_HTTP_METHODS = ("GET", "POST", "GET-PUREURL")


class EndpointAdapter:
    """
    Class to iterate over a defined API endpoint, using the 'page_arg' parameter.
    When iterated, sends requests with incrementing `page_arg` value to the specified `url` and yields json-objects as responses
    """

    def __init__(
        self,
        url: str,
        method: str,
        page_arg: Union[str, Tuple[str, int]],
        payload: Dict[str, str],
        wait_time: Union[float, Tuple[float, float]],
        parser: BaseEndpointParser,
        headers: Dict[str, str] = _DEFAULT_BASE_HEADERS,
        verbose: bool = True,
    ):
        """Initialize an EndpointAdapter to iterate over later.

        Args:
            url (str): the URL of the POST- / GET-Endpoint
            method (str): one of ("GET", "POST"). Specifies which HTTP-request type to use when contacting the endpoint
            page_arg (Union[str, Tuple[str, int]]): the name of the parameter in `payload` to increment after each request (accessing diff. pages)
                > (str): only the name of the parameter
                > (Tuple[str, int]): (name_of_parameter, first_page)
            payload (Dict[str, str]): specifies the payload to send in HTTP-request to server. The `page_arg` should be in here!
            headers (Dict[str, str], optional): The headers to send in HTTP-request. Defaults to _DEFAULT_BASE_HEADERS.
            wait_time (float): Amount of seconds to wait inbetween requests during iteration.
            verbose (bool): Whether or not logging for current status information should be enabled.

        Returns:
            EndpointAdapter: An instantiated EndpointAdapter

        Raises:
            AttributeError: raised when `method` is not a valid HTTP-request method
        """
        self.url = url
        if method.upper() not in _VALID_HTTP_METHODS:
            raise AttributeError(
                f"{method} is not a valid HTTP_METHOD! (valid methods: {_VALID_HTTP_METHODS})"
            )
        self.method = method.upper()
        if isinstance(page_arg, tuple):
            self.page_arg, self.curr_page = page_arg[0], page_arg[1]
        else:
            self.page_arg, self.curr_page = page_arg, _DEFAULT_FIRST_PAGE_NUM
        self.payload = payload
        self.headers = headers
        self.wait_time = wait_time
        assert hasattr(parser, "pipe"), "instance of `parser` has to implement `pipe`!"
        self.parser = parser
        self.verbose = verbose
        self.session = requests.Session()
        self.should_stop = False
        self._max_amount_requests = 10_000
        self.request_amount = 0

    def send_request_and_get_response(self) -> Dict[str, str]:
        """Sends a request with given `payload` to its endpoint, validates the HTTP response and returns the .json() of the response

        Returns:
            Dict[str, str]: Validated .json() field of HTTP-request
        """
        if self.method == "GET":
            print(self.url, self.payload)
            r = self.session.get(url=self.url, data=self.payload, headers=self.headers)
        elif self.method == "POST":
            r = self.session.post(url=self.url, data=self.payload, headers=self.headers)
        elif self.method == "GET-PUREURL":
            url = self.url + "?" + "&".join([f"{k}={v}" for k, v in self.payload.items()])
            r = self.session.get(url=url, headers=self.headers)

        r.raise_for_status()
        # the yielded response can now either be a dict-like object,
        # or a pure bytes-like object (raw HTML)
        try:
            # dict-like response
            return r.json()
        except:
            # raw HTML-like response
            return r.content

    def wait_remaining_time(self, start_time: float, end_time: float) -> None:
        """Waits for a certain amount of time, specified by `self.wait_time`

        Args:
            start_time (float): the time at which a given process has started.
            end_time (float): the time at which that given process ended.
        """
        time_elapsed = end_time - start_time
        if isinstance(self.wait_time, (tuple, list)):
            time_to_wait = random.uniform(*self.wait_time)
            cooldown = time_to_wait - time_elapsed
        else:
            cooldown = self.wait_time - time_elapsed
        if cooldown > 0.0:
            if self.verbose:
                print(f"\tWaiting an additional {cooldown} seconds...")
            time.sleep(cooldown)

    def __iter__(self):
        """
        Starts iteration over requests to endpoint, incrementing the `page_arg` parameter at each request.
        This loop (by default) loops infinitely, and should therefore be handled by the implementing code!
        """
        self.request_amount = 0
        self.payload[self.page_arg] = self.curr_page
        return self

    def __next__(self) -> Dict[str, str]:
        """Increments `self.page_arg` parameter at each iteration, sends a request to `self.url` and yields the result field of that response

        Returns:
            Dict[str, str]: The .json() field of resulting HTTPResponse objects
        """
        if self.should_stop:
            raise StopIteration

        start_time = time.time()
        if self.verbose:
            print(f"Sending request for page {self.payload.get(self.page_arg)}...")
        data = self.send_request_and_get_response()
        self.wait_remaining_time(start_time=start_time, end_time=time.time())

        # Handling edge case where user does not stop this iteration via `break`
        self.request_amount += 1
        if self.request_amount > self._max_amount_requests:
            raise StopIteration

        parsed_articles, self.should_stop = self.parser.pipe(data=data)
        self.payload[self.page_arg] = self.payload[self.page_arg] + 1

        return parsed_articles
