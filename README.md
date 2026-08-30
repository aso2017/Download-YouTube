# YouTube Telegram Downloader

Telegram bot that downloads single YouTube videos with yt-dlp and sends the resulting file back to the user.

## Render

1. Push these files to a GitHub repository.
2. Create a Render **Web Service** using the repository.
3. Runtime: **Docker**.
4. Add environment variable:
   - `BOT_TOKEN` = your Telegram bot token
5. Deploy.

The app exposes `/` and `/health` on Render's `$PORT` and runs Telegram polling in the same service.

## Local

```bash
pip install -r requirements.txt
python bot.py
```

FFmpeg is required for bestvideo+bestaudio merging. The included Dockerfile installs it automatically.
