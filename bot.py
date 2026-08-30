import asyncio
import os
import shutil
import uuid
from pathlib import Path

from aiohttp import web
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
COOKIE_FILE = Path("/etc/secrets/cookies.txt")


def clean_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*').strip()[:150] or "video"


def download_youtube(url: str, workdir: Path) -> tuple[Path, str]:
    template = str(workdir / "%(id)s.%(ext)s")
    opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": template,
        "noplaylist": True,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "cookiefile": str(COOKIE_FILE) if COOKIE_FILE.is_file() else None,
        "restrictfilenames": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = clean_name(info.get("title", "YouTube Video"))
        prepared = Path(ydl.prepare_filename(info))
        candidates = [prepared.with_suffix(".mp4"), prepared]
        files = [p for p in candidates if p.exists()]
        if not files:
            all_files = [p for p in workdir.iterdir() if p.is_file()]
            if not all_files:
                raise FileNotFoundError("Downloaded file was not found")
            files.sort(key=lambda p: p.stat().st_size, reverse=True)
            return files[0], title
        return files[0], title


async def health(request):
    return web.json_response({"status": "ok", "service": "youtube-telegram-bot"})


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"Health server listening on {port}")


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n\nلینک YouTube رو بفرست تا ویدئو رو دانلود کنم 🎬\n\n"
        "فقط لینک ویدئوی تکی بفرست؛ پلی‌لیست پشتیبانی نمی‌شود."
    )


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    url = update.message.text.strip()
    if "youtube.com/" not in url and "youtu.be/" not in url:
        await update.message.reply_text("❌ لطفاً یک لینک معتبر YouTube بفرست.")
        return

    status = await update.message.reply_text("⏳ در حال دریافت اطلاعات و دانلود...")
    workdir = DOWNLOAD_DIR / uuid.uuid4().hex
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        loop = asyncio.get_running_loop()
        file_path, title = await loop.run_in_executor(None, download_youtube, url, workdir)
        await status.edit_text("📤 دانلود انجام شد؛ در حال ارسال فایل...")
        caption = f"🎬 {title}"
        with file_path.open("rb") as f:
            await update.message.reply_document(document=f, filename=file_path.name, caption=caption[:1024])
        await status.delete()
    except Exception as e:
        print("DOWNLOAD ERROR:", repr(e))
        text = str(e).strip() or "خطای نامشخص"
        await status.edit_text(f"❌ دانلود انجام نشد.\n\n{text[:1800]}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing")

    print(f"YouTube cookies: {'enabled' if COOKIE_FILE.is_file() else 'not configured'}")
    await start_web_server()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    print("Telegram bot is running")
    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
