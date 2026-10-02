"""Offline tests; mock yt-dlp so no account or network access is needed."""
import asyncio
import importlib
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# These tests verify our integration, not yt-dlp's external behavior.
with patch.dict(sys.modules, {"yt_dlp": types.SimpleNamespace(YoutubeDL=MagicMock())}):
    cookies = importlib.import_module("services.cookies")
    youtube_module = importlib.import_module("services.youtube")
    extractor_module = importlib.import_module("services.extractor")
    downloader_module = importlib.import_module("services.downloader")


class CookieTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.app = self.root / "music-api"
        self.app.mkdir()
        self.paths = patch.object(cookies, "APP_DIR", self.app)
        self.paths.start()
        self.addCleanup(self.paths.stop)
        self.env = patch.dict(os.environ, {"YOUTUBE_COOKIES": ""})
        self.env.start()
        self.addCleanup(self.env.stop)
        cookies._environment_cookie_path = None

    def write_cookies(self, directory):
        path = directory / "cookis.txt"
        path.write_text("# Netscape HTTP Cookie File\n", encoding="utf-8")
        return str(path)

    def test_missing_file_is_explicit(self):
        with self.assertRaisesRegex(FileNotFoundError, "Missing cookis.txt"):
            cookies.cookie_options()

    def test_empty_file_is_explicit(self):
        (self.app / "cookis.txt").touch()
        with self.assertRaisesRegex(ValueError, "empty"):
            cookies.cookie_options()

    def test_root_file_and_app_precedence(self):
        root_path = self.write_cookies(self.root)
        self.assertEqual(cookies.cookie_options(), {"cookiefile": root_path})
        app_path = self.write_cookies(self.app)
        self.assertEqual(cookies.cookie_options(), {"cookiefile": app_path})

    def test_file_can_be_added_after_missing_request(self):
        with self.assertRaises(FileNotFoundError):
            cookies.cookie_options()
        path = self.write_cookies(self.app)
        self.assertEqual(cookies.cookie_options()["cookiefile"], path)

    def test_path_is_independent_of_working_directory(self):
        path = self.write_cookies(self.app)
        with patch("os.getcwd", return_value="/unrelated"):
            self.assertEqual(cookies.cookie_options()["cookiefile"], path)

    def test_environment_cookies_are_written_to_a_private_temp_file(self):
        self.env.stop()
        self.env = patch.dict(
            os.environ,
            {"YOUTUBE_COOKIES": "# Netscape HTTP Cookie File\nexample.test\tTRUE\t/\tTRUE\t0\tname\tvalue\n"},
        )
        self.env.start()
        self.addCleanup(self.env.stop)

        path = Path(cookies.cookie_options()["cookiefile"])
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        self.assertTrue(path.is_file())
        self.assertEqual(path.read_text(encoding="utf-8").splitlines()[0], "# Netscape HTTP Cookie File")
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_environment_cookies_require_netscape_format(self):
        self.env.stop()
        self.env = patch.dict(os.environ, {"YOUTUBE_COOKIES": "not a cookie file"})
        self.env.start()
        self.addCleanup(self.env.stop)

        with self.assertRaisesRegex(ValueError, "Netscape-format"):
            cookies.cookie_options()

    def test_all_youtube_operations_pass_cookies(self):
        path = self.write_cookies(self.app)
        operations = [
            (youtube_module, youtube_module.youtube.search, "test"),
            (extractor_module, extractor_module.extractor.get_stream, "test-id"),
            (downloader_module, downloader_module.downloader.download, "dQw4w9WgXcQ"),
        ]
        for module, operation, argument in operations:
            with self.subTest(operation=operation.__name__):
                with patch.object(module, "YoutubeDL") as factory:
                    client = factory.return_value.__enter__.return_value
                    client.extract_info.return_value = {"id": "test-id", "entries": []}
                    asyncio.run(operation(argument))
                    self.assertEqual(factory.call_args.args[0]["cookiefile"], path)
                    self.assertEqual(
                        factory.call_args.args[0]["js_runtimes"],
                        {"node": {}}
                    )
                    client.extract_info.assert_called_once()

    def test_downloader_searches_for_song_name_then_downloads_result(self):
        cookie_path = self.write_cookies(self.app)
        with patch.object(downloader_module, "YoutubeDL") as factory:
            client = factory.return_value.__enter__.return_value
            client.extract_info.side_effect = [
                {"entries": [{"id": "dQw4w9WgXcQ", "title": "Example Song"}]},
                {"id": "dQw4w9WgXcQ", "title": "Example Song"},
            ]
            client.prepare_filename.return_value = "downloads/dQw4w9WgXcQ.webm"

            result = asyncio.run(downloader_module.downloader.download("12saal"))

            self.assertEqual(result["id"], "dQw4w9WgXcQ")
            self.assertEqual(
                client.extract_info.call_args_list[0].args[0],
                "ytsearch1:12saal"
            )
            self.assertFalse(client.extract_info.call_args_list[0].kwargs["download"])
            self.assertEqual(
                client.extract_info.call_args_list[1].args[0],
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
            self.assertTrue(client.extract_info.call_args_list[1].kwargs["download"])
            for call in factory.call_args_list:
                self.assertEqual(call.args[0]["cookiefile"], cookie_path)
                self.assertEqual(call.args[0]["js_runtimes"], {"node": {}})

    def test_explicit_search_accepts_an_eleven_character_song_name(self):
        self.write_cookies(self.app)
        with patch.object(downloader_module, "YoutubeDL") as factory:
            client = factory.return_value.__enter__.return_value
            client.extract_info.side_effect = [
                {"entries": [{"id": "dQw4w9WgXcQ"}]},
                {"id": "dQw4w9WgXcQ", "title": "Example Song"},
            ]
            client.prepare_filename.return_value = "downloads/dQw4w9WgXcQ.webm"

            asyncio.run(
                downloader_module.downloader.download("songtitle12", search=True)
            )

            self.assertEqual(
                client.extract_info.call_args_list[0].args[0],
                "ytsearch1:songtitle12"
            )


if __name__ == "__main__":
    unittest.main()
