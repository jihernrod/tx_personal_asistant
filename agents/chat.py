from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
from telegram import Bot
import chatbot

CHAT_ID = 5224270604
API_TOKEN = '7922946027:AAFeKpf6V0ci2q8luAHAZydlXvLhDtNKD6E'

bot = Bot(token=API_TOKEN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user.username
    text = update.message.text

    print(f"Mensaje recibido de @{user} en chat {chat_id}: {text}")
    try:
        msg_response = await chatbot.chat(text)
    except:
        msg_response = "Debes hacer preguntas financieras que tengan mas sentido"
    print ("#####"+msg_response+"#####")
    await bot.send_message(chat_id=CHAT_ID, text=msg_response)

app = ApplicationBuilder().token(API_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Inicia el bot
print("Bot escuchando mensajes...")
app.run_polling()