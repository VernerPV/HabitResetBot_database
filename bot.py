import os
from telegram.ext import ContextTypes, Application
BOT_TOKEN = os.environ['BOT_TOKEN']
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
 await context.bot.send_message(chat_id=838386449, text='One message every minute')

application = Application.builder().token(BOT_TOKEN).build()
job_queue = application.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)

application.run_polling()