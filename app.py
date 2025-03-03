import requests
import uvicorn
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler

# Token bot Telegram
TOKEN = "7898028279:AAF9nIlja0DnvS179zFeKbqqD5ZB_aICP8o"

# Địa chỉ ví Zpool cần kiểm tra
WALLET = "RMfMCKAUvrQUxBz1fwSEVfkeDQJZAQGzzs"

# API URL của Zpool
ZPOOL_API = f"https://www.zpool.ca/api/wallet?address={WALLET}"

# Tạo bot Telegram
bot_app = Application.builder().token(TOKEN).build()

# FastAPI server
server = FastAPI()

# Hàm kiểm tra trạng thái mining
async def mining(update: Update, context):
    try:
        response = requests.get(ZPOOL_API).json()
        
        hashrate = response.get("hashrate", 0)
        balance = response.get("confirmed", 0)
        unpaid = response.get("unconfirmed", 0)
        workers = response.get("workers", 0)
        
        message = (
            f"💎 **Trạng thái Mining Zpool** 💎\n"
            f"⚡ Hashrate: `{hashrate:.2f} H/s`\n"
            f"💰 Số dư: `{balance:.8f} RVN`\n"
            f"🕐 Chưa xác nhận: `{unpaid:.8f} RVN`\n"
            f"👷 Worker đang hoạt động: `{workers}`"
        )
        
    except Exception as e:
        message = f"❌ Lỗi khi lấy dữ liệu từ Zpool: {e}"
    
    await update.message.reply_text(message, parse_mode="Markdown")

# Thêm lệnh /mining vào bot
bot_app.add_handler(CommandHandler("mining", mining))

# API kiểm tra trạng thái bot
@server.get("/")
def read_root():
    return {"status": "Bot đang chạy trên Hugging Face Spaces!"}

# Chạy bot Telegram song song với FastAPI
async def run_bot():
    await bot_app.run_polling()

# Chạy cả bot và FastAPI server
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(run_bot())  # Chạy bot Telegram trong nền
    uvicorn.run(server, host="0.0.0.0", port=10000)  # Chạy FastAPI server
