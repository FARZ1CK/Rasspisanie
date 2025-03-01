import req
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
import logging
import datetime
from telegram.ext import JobQueue

def check(current_time):
    if current_time.hour == 7 and current_time.minute == 0:
        return True
    return False

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = req.TOKEN
application = ApplicationBuilder().token(TOKEN).build()

rassp = req.rassp

async def start(update: Update, context):
    await update.message.reply_text("Привет! Теперь я работаю!")
    # Используем `data` для передачи chat_id в задачу
    context.job_queue.run_repeating(send_schedule, interval=60.0, first=0.0, data=update.message.chat_id)

async def send_schedule(context):
    current_time = datetime.datetime.now().time()
    current_dayt = datetime.datetime.today()
    if check(current_time):
        day_of_week = current_dayt.weekday()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        # Получаем chat_id из context.job.data
        chat_id = context.job.data
        await context.bot.send_message(chat_id=chat_id, text=rassp.get(days[day_of_week]))

application.add_handler(CommandHandler('start', start))
application.run_polling()