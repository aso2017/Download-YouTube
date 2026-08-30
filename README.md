# YouTube Telegram Downloader — Render

Telegram bot using `yt-dlp`, ready for Render Docker Web Service.

## Render setup

1. Create a **Web Service** from this repository.
2. Runtime: **Docker**. Do not enter Build Command or Start Command; the Dockerfile handles them.
3. Add environment variable:
   - `BOT_TOKEN` = your Telegram bot token.
4. Add a Render **Secret File**:
   - Filename/path: `cookies.txt`
   - Contents: your valid Mozilla/Netscape-format YouTube cookies.
5. The app reads the secret from `/etc/secrets/cookies.txt` automatically.
6. Deploy.

The app exposes `/` and `/health` on Render's `$PORT` and starts Telegram polling.

## Cookie format

The cookie file must be Mozilla/Netscape format and should begin with either:

`# HTTP Cookie File`

or

`# Netscape HTTP Cookie File`

Keep cookies private. Never commit `cookies.txt` to GitHub.

## Local test

```bash
pip install -r requirements.txt
python bot.py
```

Set `BOT_TOKEN` before running locally.
