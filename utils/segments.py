import json
import urllib.parse
from typing import *

import requests

import config

__all__ = [
    "get_segments", "Segment"
]

Segment = Tuple[float, float]


def build_segments_url(video_id: str) -> str:
    query_params = {
        "videoID": video_id,
        "categories": json.dumps(config.SEGMENTS_CATEGORIES)
    }
    query = "?" + urllib.parse.urlencode(query_params)
    # API needs unquoted query
    query = urllib.parse.unquote_plus(query)
    url = f"{config.SEGMENTS_API_URL}{query}"
    
    return url


def parse_segment(data: List[dict]) -> List[Segment]:
    return [
        (element["segment"][0], element["segment"][1])
        for element in data
    ]


def get_segments(video_id: str) -> List[Segment]:
    url = build_segments_url(video_id)
    response = requests.get(url)
    
    if not (200 <= response.status_code < 300):
        return []
    
    segments = parse_segment(response.json())
    
    return segments
