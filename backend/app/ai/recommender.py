"""
DEPRECATED: Use ai_service.py -> video_recommender.py (YouTube hybrid).
"""

import requests
import os

class Recommender:
    """Recommend study materials"""
    
    @staticmethod
    def search_youtube_videos(topic: str, max_results: int = 10) -> dict:
        """
        Search for educational YouTube videos using AI recommendations
        
        Args:
            topic (str): Search topic/keywords
            max_results (int): Maximum number of results (1-20)
            
        Returns:
            dict: Video recommendations
        """
        # Use AI to generate video recommendations (no API key needed!)
        from app.ai.groq_client import get_groq_client
        
        try:
            client = get_groq_client()
            
            prompt = f"""Generate {max_results} popular and highly-rated educational YouTube video recommendations for the topic: "{topic}".

For each video, provide:
1. A realistic video title
2. Channel name (use real popular educational channels when possible)
3. Estimated duration (format: MM:SS)
4. Brief description

Format as JSON array:
[
  {{
    "title": "Video title",
    "channel": "Channel name",
    "duration": "15:30",
    "description": "Brief description"
  }}
]

Focus on well-known educational channels like Khan Academy, Crash Course, freeCodeCamp, MIT OpenCourseWare, 3Blue1Brown, etc.

Videos:"""

            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse JSON response
            import json
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                videos_data = json.loads(json_str)
                
                # Format videos with YouTube search URLs
                videos = []
                for idx, video in enumerate(videos_data[:max_results]):
                    search_query = f"{video.get('title', topic)} {video.get('channel', '')}"
                    # Use a better placeholder service with YouTube-style thumbnails
                    thumbnail_text = video.get('title', 'Video')[:30].replace(' ', '+')
                    videos.append({
                        'title': video.get('title', f'{topic} Tutorial'),
                        'channel': video.get('channel', 'Educational Channel'),
                        'thumbnail': f'https://img.youtube.com/vi/placeholder/mqdefault.jpg',  # YouTube default thumbnail
                        'url': f'https://youtube.com/results?search_query={search_query.replace(" ", "+")}',
                        'duration': video.get('duration', '15:00'),
                        'description': video.get('description', 'Educational video')
                    })
                
                return {
                    'videos': videos,
                    'total_results': len(videos),
                    'search_query': topic,
                    'note': 'AI-generated recommendations. Click to search on YouTube.'
                }
            else:
                raise ValueError("Could not parse AI response")
                
        except Exception as e:
            # Fallback to simple recommendations
            return {
                'videos': [
                    {
                        'title': f'{topic} - Complete Tutorial',
                        'channel': 'freeCodeCamp',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+tutorial',
                        'duration': '15:30',
                        'description': 'Comprehensive tutorial'
                    },
                    {
                        'title': f'{topic} - Crash Course',
                        'channel': 'Crash Course',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+crash+course',
                        'duration': '12:45',
                        'description': 'Quick overview'
                    },
                    {
                        'title': f'{topic} Explained',
                        'channel': 'Khan Academy',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+explained',
                        'duration': '10:20',
                        'description': 'Clear explanation'
                    }
                ],
                'total_results': 3,
                'search_query': topic,
                'note': 'Showing recommended searches. Click to find videos on YouTube.'
            }
        
        try:
            # Make API request to YouTube
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': topic + ' tutorial education',
                'type': 'video',
                'maxResults': min(max_results, 20),
                'key': youtube_api_key,
                'videoDuration': 'medium',  # 4-20 minutes
                'order': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                videos.append({
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'description': snippet['description'][:200] + '...',
                    'published_at': snippet['publishedAt']
                })
            
            return {
                'videos': videos,
                'total_results': len(videos),
                'search_query': topic
            }
            
        except Exception as e:
            raise Exception(f"Failed to search YouTube: {str(e)}")
    
    @staticmethod
    def recommend_resources(topic: str) -> dict:
        """
        Recommend various study resources
        
        Args:
            topic (str): Study topic
            
        Returns:
            dict: Recommended resources with videos array
        """
        try:
            # Get YouTube videos using AI
            youtube_results = Recommender.search_youtube_videos(topic, max_results=8)
            
            # Return in format expected by frontend (videos array)
            return {
                'videos': youtube_results['videos'],
                'total_results': youtube_results['total_results'],
                'search_query': topic,
                'note': youtube_results.get('note', 'AI-generated recommendations')
            }
            
        except Exception as e:
            # Return fallback recommendations
            return {
                'videos': [
                    {
                        'title': f'{topic} - Complete Tutorial',
                        'channel': 'freeCodeCamp',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+tutorial',
                        'duration': '15:30',
                        'description': 'Comprehensive tutorial'
                    },
                    {
                        'title': f'{topic} - Crash Course',
                        'channel': 'Crash Course',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+crash+course',
                        'duration': '12:45',
                        'description': 'Quick overview'
                    },
                    {
                        'title': f'{topic} Explained',
                        'channel': 'Khan Academy',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+explained',
                        'duration': '10:20',
                        'description': 'Clear explanation'
                    },
                    {
                        'title': f'Learn {topic} in 2024',
                        'channel': 'Programming with Mosh',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query=learn+{topic.replace(" ", "+")}+2024',
                        'duration': '18:15',
                        'description': 'Modern approach'
                    },
                    {
                        'title': f'{topic} for Beginners',
                        'channel': 'Traversy Media',
                        'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+for+beginners',
                        'duration': '20:00',
                        'description': 'Beginner-friendly'
                    }
                ],
                'total_results': 5,
                'search_query': topic,
                'note': 'Showing recommended searches. Click to find videos on YouTube.'
            }
