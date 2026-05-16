"""
YouTube Video Recommender - uses YouTube Data API when key is set, else search fallback
"""

import os
import requests
from youtubesearchpython import VideosSearch


class VideoRecommender:
    def recommend_videos(self, topic: str, max_results: int = 10) -> dict:
        api_key = os.getenv('YOUTUBE_API_KEY')
        if api_key:
            return self._search_via_api(topic, max_results, api_key)
        return self._search_via_scraper(topic, max_results)

    def _search_via_api(self, topic: str, max_results: int, api_key: str) -> dict:
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': f'{topic} tutorial education',
            'type': 'video',
            'maxResults': min(max_results, 20),
            'key': api_key,
            'videoDuration': 'medium',
            'order': 'relevance',
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            thumbnails = snippet.get('thumbnails', {})
            thumb = thumbnails.get('medium') or thumbnails.get('default') or {}
            videos.append({
                'title': snippet['title'],
                'channel': snippet['channelTitle'],
                'thumbnail': thumb.get('url', ''),
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'duration': '',
                'description': snippet.get('description', '')[:200],
            })

        return {
            'videos': videos,
            'total_results': len(videos),
            'search_query': topic,
            'source': 'youtube_api',
        }

    def _search_via_scraper(self, topic: str, max_results: int) -> dict:
        try:
            search = VideosSearch(f"{topic} tutorial for beginners", limit=max_results)
            results = search.result()

            videos = []
            for video in results.get('result', []):
                videos.append({
                    'title': video.get('title', f'{topic} Tutorial'),
                    'channel': video.get('channel', {}).get('name', 'YouTube Channel'),
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url', ''),
                    'url': video.get('link', ''),
                    'duration': video.get('duration', '10:00'),
                    'views': video.get('viewCount', {}).get('short', '0'),
                })

            return {
                'videos': videos,
                'total_results': len(videos),
                'search_query': topic,
                'source': 'youtube_search',
            }
        except Exception as e:
            return {
                'videos': [],
                'total_results': 0,
                'error': str(e),
            }


_video_recommender = None


def get_video_recommender():
    global _video_recommender
    if _video_recommender is None:
        _video_recommender = VideoRecommender()
    return _video_recommender
