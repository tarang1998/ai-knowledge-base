# Required : Python 3.7

import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Reference:
    '''
    A class to store previously response from the openai API
    '''

    def __init__(self) -> None:
        self.response = ""



reference = Reference()
model_name = "gpt-3.5-turbo"



# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)



def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("The past conversation and context are cleared.")



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Zues Bot!\nCreated by Tarang. How can i assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Zues bot created by Tarang! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)





@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")

    response = openai.chat.completions.create(
        model = model_name,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)


