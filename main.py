from config import prop
from api import telegram
import os
from tx_agents import chatbot

print(prop.secrets().chat_id)
print(prop.secrets().api_token)
print(prop.secrets().api_key)


os.environ['OPENAI_API_KEY'] = prop.secrets().api_key

telegram.bot(prop.secrets().chat_id,
            prop.secrets().api_token,
             chatbot.chat).run_polling()

