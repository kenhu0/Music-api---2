from yt_dlp import YoutubeDL
from .cookies import cookie_options
from .yt_dlp_options import js_runtime_options


class StreamExtractor:

    def __init__(self):

        self.options = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            **js_runtime_options()
        }

    async def get_stream(self, video_id: str):

        url = f"https://www.youtube.com/watch?v={video_id}"

        with YoutubeDL({**self.options, **cookie_options()}) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "channel_id": info.get("channel_id"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "upload_date": info.get("upload_date"),
            "description": info.get("description"),
            "tags": info.get("tags"),
            "thumbnail": info.get("thumbnail"),
            "stream_url": info.get("url"),
            "webpage_url": info.get("webpage_url")
        }


extractor = StreamExtractor()