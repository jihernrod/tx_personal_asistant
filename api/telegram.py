from typing import Callable

from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
from telegram import Bot
from metaclases import Singleton as mtc


class TelegramBotHandler(metaclass=mtc.SingletonMeta):

    def __init__(self, bot: Bot, chat_id: int, _delegate_functor:Callable):
        self._bot = bot
        self._chat_id = chat_id
        self._delegate_functor = _delegate_functor

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        user = update.effective_user.username
        text = update.message.text

        print(f"Mensaje recibido de @{user} en chat {self._chat_id}: {text}")
        try:
            msg_response = await self._delegate_functor(text)
        except:
            msg_response = "Debes hacer preguntas financieras que tengan mas sentido"
        print ("#####"+msg_response+"#####")

        await self._bot.send_message(chat_id=self._chat_id, text=msg_response)


def bot(chat_id: int, api_token: str, delegate_functor: Callable):
    tb = TelegramBotHandler(Bot(token=api_token), chat_id, delegate_functor)
    app = ApplicationBuilder().token(api_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tb.handle_message))
    return app

