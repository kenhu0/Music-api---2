from datetime import timedelta


def format_duration(seconds):

    if not seconds:
        return "00:00"

    return str(timedelta(seconds=int(seconds)))


def thumbnail(video_id, quality="hq"):

    qualities = {
        "default": "default",
        "medium": "mqdefault",
        "high": "hqdefault",
        "sd": "sddefault",
        "max": "maxresdefault"
    }

    q = qualities.get(quality, "hqdefault")

    return f"https://i.ytimg.com/vi/{video_id}/{q}.jpg"


def youtube_url(video_id):

    return f"https://www.youtube.com/watch?v={video_id}"


def is_valid_video_id(video_id):

    return isinstance(video_id, str) and len(video_id) == 11


def success(data):

    return {
        "success": True,
        "credits": "WLZBI",
        "result": data
    }


def error(message):

    return {
        "success": False,
        "credits": "WLZBI",
        "error": message
    }