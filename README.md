# YouTube Telegram Downloader — Render

Telegram bot using `yt-dlp`, Deno and FFmpeg, ready for Render Docker Web Service.

## Render setup

1. Create a **Web Service** from this repository.
2. Runtime: **Docker**. Do not enter a Build Command or Start Command; the Dockerfile handles both.
3. Add environment variable:
   - `BOT_TOKEN` = your Telegram bot token.
4. Add a Render **Secret File**:
   - **Filename/path:** `/etc/secrets/cookies.txt`
   - **Contents:** your valid Mozilla/Netscape-format YouTube cookies.
5. Deploy.

The app automatically reads the cookie file from `/etc/secrets/cookies.txt`. No Base64 conversion is required, and the cookie file must never be committed to GitHub.

## Runtime and storage

- Downloads are stored under `/tmp/downloads` so the app does not depend on a writable path inside the application image.
- Deno is installed in the Docker image for YouTube JavaScript challenge solving.
- `yt-dlp` is configured to use Deno and the remote `yt-dlp-ejs` component from GitHub when needed.
- FFmpeg is installed for video/audio merging and MP4 output.
- Each download gets its own temporary work directory.
- The temporary directory is deleted automatically after the Telegram upload succeeds or fails.
- The app exposes `/` and `/health` on Render's `$PORT` and starts Telegram polling.

## Cookie format

The cookie file must be in Mozilla/Netscape format and should begin with either:

`# HTTP Cookie File`

or

`# Netscape HTTP Cookie File`

Keep cookies private. Never commit `cookies.txt` to GitHub.

## Local test

```bash
pip install -r requirements.txt
```

Set `BOT_TOKEN` before running:

```bash
# Windows PowerShell
$env:BOT_TOKEN="YOUR_BOT_TOKEN"
python bot.py
```

For a local cookie file, change the `COOKIE_FILE` path temporarily or mount/copy the file to `/etc/secrets/cookies.txt` in your test environment.

## Render checklist

- `BOT_TOKEN` is configured in Environment Variables.
- Secret File exists at exactly `/etc/secrets/cookies.txt`.
- Cookie contents are valid and current.
- Service type is **Web Service** with **Docker** runtime.
- No separate Start Command overrides the Dockerfile.
