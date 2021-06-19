from typing import *
from dataclasses import dataclass, field

import requests
from requests import HTTPError

__all__ = [
    "AllInstancesFailed", "InvidiousAPI", "instance"
]

from requests.exceptions import RequestException, SSLError

INSTANCE_TYPE = "https"


class AllInstancesFailed(HTTPError):
    pass


def get_instance_urls() -> List[str]:
    response = requests.get("https://api.invidious.io/instances.json")

    response.raise_for_status()

    instances = response.json()
    urls = [
        data["uri"]
        for (name, data) in instances
        if data["type"] == INSTANCE_TYPE
    ]

    return urls


@dataclass
class InvidiousAPI:
    instance_urls: List[str] = field(default_factory=get_instance_urls)

    def get(self, endpoint: str):
        for url in self.instance_urls:
            api_url = url + endpoint

            try:
                result = requests.get(api_url)
            except RequestException:
                continue

            if not (200 <= result.status_code < 300):
                continue

            return result.json()

        raise AllInstancesFailed()


instance = InvidiousAPI()
