from pathlib import Path
import re
from yt_dlp import YoutubeDL
from .cookies import cookie_options
from .yt_dlp_options import js_runtime_options

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


class Downloader:

    def __init__(self):

        self.options = {
            "format": "bestaudio/best",
            "outtmpl": str(DOWNLOAD_DIR / "%(id)s.%(ext)s"),
            "quiet": True,
            "noplaylist": True,
            **js_runtime_options()
        }

    async def download(self, video_id_or_query: str, *, search: bool = False):
        value = video_id_or_query.strip()
        if not value:
            raise ValueError("Provide a YouTube video ID or song name.")

        video_id = value
        if search or not VIDEO_ID_PATTERN.fullmatch(value):
            search_options = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "skip_download": True,
                **js_runtime_options(),
                **cookie_options()
            }

            with YoutubeDL(search_options) as ydl:
                results = ydl.extract_info(f"ytsearch1:{value}", download=False)

            first_result = next(
                (entry for entry in (results or {}).get("entries", []) if entry),
                None
            )
            video_id = first_result.get("id") if first_result else None
            if not video_id:
                raise ValueError(f"No YouTube results found for '{value}'.")

        url = f"https://www.youtube.com/watch?v={video_id}"
        with YoutubeDL({**self.options, **cookie_options()}) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "filename": filename
        }


downloader = Downloader()