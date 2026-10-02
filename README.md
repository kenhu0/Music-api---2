# music-api
🎵 A powerful FastAPI-based music API for searching, streaming, downloading, lyrics, playlists and more. Built with Python and designed for music bots, apps, and automation projects.

# 🎵 Music API

<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/SQLite-Database-orange?style=for-the-badge&logo=sqlite">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">

</p>

<p align="center">

<img src="https://img.shields.io/github/stars/wlzbi-exe/music-api?style=for-the-badge&logo=github">

</p>


## 🎧 About

A powerful, lightweight and developer-friendly Music API built with **FastAPI + Python**.

This API provides music search, streaming, playback, downloading, lyrics, playlists and more.

Designed for developers who want to integrate music features into:

- 🤖 Telegram Bots
- 🌐 Websites
- 📱 Applications
- ⚙️ Automation Tools


---

# ✨ Features

- 🎧 Music Search API
- 🔊 Audio Streaming
- ▶️ Music Playback System
- 📥 Download Support
- 🎤 Lyrics Fetching
- 📀 Playlist Management
- 🔐 Authentication System
- 📊 API Statistics
- ❤️ Health Monitoring
- ⚡ Cache System
- 📝 Logging System


---

# 🚀 Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite Database
- Async API Architecture
- YouTube Music Extraction
- Custom Cache System


---

# 📂 Project Structure

```text
music-api/
│
├── app.py
├── config.py
├── requirements.txt
├── database.py
│
├── routes/
│   ├── __init__.py
│   ├── search.py
│   ├── stream.py
│   ├── play.py
│   ├── download.py
│   ├── lyrics.py
│   ├── playlist.py
│   ├── auth.py
│   ├── stats.py
│   └── health.py
│
├── services/
│   ├── __init__.py
│   ├── youtube.py
│   ├── extractor.py
│   ├── downloader.py
│   ├── lyrics.py
│   ├── cache.py
│   ├── auth.py
│   ├── logger.py
│   └── utils.py
│
├── cache/
├── downloads/
├── database/
├── logs/
│
└── README.md
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/wlzbi-exe/music-api.git
```

```bash
cd music-api
```

### Install Requirements

```bash
pip install -r requirements.txt
```


---

# ▶️ Run API

### YouTube cookies

Search, streaming, playback, song details, and downloads now require a
`cookis.txt` file containing valid YouTube cookies in **Netscape cookie-file
format** (not JSON). Put it in `music-api/cookis.txt` or in the repository root.
On Railway, set a private multiline service variable named `YOUTUBE_COOKIES`
to the full cookie-file contents, including its Netscape header. The API writes
that value to a permission-restricted temporary file for yt-dlp and removes it
when the process exits. This variable takes priority over local cookie files.
Paths work independently of the directory from which the API is started.

Export cookies from your own authorized YouTube browser session using a
trusted tool. Cookie files contain session credentials: do not paste them into
chat, share them, or commit them. Both `cookis.txt` and `cookies.txt` are ignored
by Git, but only the requested filename `cookis.txt` is loaded. Keep the
workspace private when storing cookies in it.

The file is checked on each YouTube request, so it can be added or replaced
without restarting the API. Missing or empty files produce an explicit error.
Expired or invalid cookies must be replaced. Valid cookies may help with
YouTube's “Sign in to confirm you're not a bot” error, but YouTube may still
block requests because of IP reputation or other restrictions; cookies cannot
guarantee access. Respect YouTube's terms and content permissions.

YouTube extraction also requires yt-dlp's JavaScript challenge solver and a
supported JavaScript runtime. The `yt-dlp[default]` dependency installs the
solver scripts, and this workspace enables Node.js 22+. Other hosting
environments must provide Node.js 22 or newer on `PATH`.

Start the server:

```bash
cd music-api
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Deploy to Railway from GitHub

1. Push this repository to GitHub.
2. In Railway, create a project using **Deploy from GitHub Repo**, then select
   this repository and the branch to deploy.
3. In the service's **Settings**, set the root directory to `/music-api`.
4. Add these service variables:
   - `RAILPACK_PACKAGES` = `node@22` (yt-dlp needs Node.js for YouTube challenge solving).
   - `YOUTUBE_COOKIES` = your complete Netscape-format cookie file contents.
     Keep this variable private; do not commit cookies to GitHub or paste them
     into chat.
5. Set the start command to
   `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`.
6. Deploy the service, then generate a public domain in **Settings → Networking**.
   The API docs are available at `/docs`, and `/health` can be used as the
   health-check path.

Railway deploys new commits from the connected branch automatically. Check
the service's deployment logs if the build or startup fails.

API:

```
http://localhost:8000
```

Swagger Docs:

```
http://localhost:8000/docs
```


---

# 🔥 API Endpoints

## ❤️ Health Check

```
GET /health
```


## 🎵 Search Music

```
GET /search?q=query
```


## 🔊 Stream Music

```
GET /stream/{id}
```


## ▶️ Play Music

```
GET /play/{id}
```

## 📥 Download Audio

Use a YouTube video ID:

```
GET /download?id=VIDEO_ID
```

Or search by song name:

```
GET /download?q=SONG_NAME
```

The `id` parameter also accepts a song name when the value is not an 11-character YouTube video ID. Requests require valid YouTube cookies.


---

# 🛣️ Roadmap

- ✅ Search API
- ✅ Streaming API
- ✅ Play API
- ✅ Download API (video ID or song-name search)
- ⏳ Lyrics API
- ⏳ Playlist System
- ⏳ Authentication
- ⏳ User Statistics
- ⏳ Cloud Storage Support


---

# 🤝 Contributing

Contributions are welcome!

Steps:

1. Fork this repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request


---

# ⚠️ Disclaimer

This project is created for educational and development purposes.

Users are responsible for respecting copyright rules and external platform terms.


---

# 📜 License

Licensed under the MIT License.


---

# ⭐ Support

If you find this project useful, consider giving it a star ⭐ on GitHub.


---

# 👨‍💻 Developer

<p align="center">

<img src="https://img.shields.io/badge/DEV-WLZBI-black?style=for-the-badge&logo=github">

</p>


<p align="center">

<a href="https://github.com/wlzbi-exe">
<img src="https://img.shields.io/badge/GitHub-wlzbi--exe-181717?style=for-the-badge&logo=github">
</a>

<a href="https://t.me/rejerks">
<img src="https://img.shields.io/badge/Telegram-@rejerks-26A5E4?style=for-the-badge&logo=telegram">
</a>

</p>


<p align="center">
BY <b>WLZBI</b>
</p>
