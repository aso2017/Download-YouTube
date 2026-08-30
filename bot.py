
import os
import asyncio
import shutil
import uuid
import subprocess
from pathlib import Path
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = Path("/tmp/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

COOKIE_FILE = Path("/app/cookies.txt")
PORT = int(os.getenv("PORT", "10000"))

def download(url, folder):
    out = str(folder / "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--cookies", str(COOKIE_FILE),
        "--js-runtimes", "deno",
        "--remote-components", "ejs:github",
        "--no-playlist",
        "-o", out,
        url
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    files = list(folder.glob("*"))
    return max(files, key=lambda x:x.stat().st_size)

async def health(request):
    return web.json_response({"ok": True})

async def server():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()

async def start(update: Update, context):
    await update.message.reply_text("لینک یوتیوب را بفرست")

async def handle(update: Update, context):
    url = update.message.text
    msg = await update.message.reply_text("در حال دانلود...")
    folder = DOWNLOAD_DIR / uuid.uuid4().hex
    folder.mkdir()
    try:
        loop = asyncio.get_running_loop()
        f = await loop.run_in_executor(None, download, url, folder)
        with f.open("rb") as x:
            await update.message.reply_document(x, filename=f.name)
    except Exception as e:
        await msg.edit_text(str(e)[:1000])
    finally:
        shutil.rmtree(folder, ignore_errors=True)

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN missing")
    await server()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
