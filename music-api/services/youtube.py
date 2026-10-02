from yt_dlp import YoutubeDL
from .cookies import cookie_options
from .yt_dlp_options import js_runtime_options

class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
            "default_search": "ytsearch",
            **js_runtime_options()
        }

    async def search(self, query: str, limit: int = 10):
        with YoutubeDL({**self.ydl_opts, **cookie_options()}) as ydl:
            info = ydl.extract_info(
                f"ytsearch{limit}:{query}",
                download=False
            )

        results = []

        for video in info.get("entries", []):
            if not video:
                continue

            results.append({
                "id": video.get("id"),
                "title": video.get("title"),
                "channel": video.get("uploader"),
                "duration": video.get("duration"),
                "thumbnail": (
                    f"https://i.ytimg.com/vi/{video.get('id')}/hqdefault.jpg"
                    if video.get("id") else None
                ),
                "url": (
                    f"https://youtube.com/watch?v={video.get('id')}"
                    if video.get("id") else None
                )
            })

        return results


youtube = YouTubeService()