#from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import choice
from pyrogram import Client, filters, idle
#from aiohttp import ClientSession
#from json import loads
#from pyrogram.types import Message as message
import asyncio
#import openai
import requests
import logging
import os

GOOGLEAI_KEY = "AIzaSyC2cKZRxUsoCfYaveyab08QEp7jxsRWrJk"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("gptbot", bot_token="6560962385:AAHwbTlxi7ntT6y6c8rfgu4_zgXw9y2vq2Q", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")

@app.on_message(filters.command("ask"))
async def gemini_chatbot(_, message):
    if len(message.command) == 1:
        return await message.reply_message("Please ask a question")
    if not GOOGLEAI_KEY:
        return await message.reply_msg("GOOGLEAI_KEY env is missing!!!")
    msg = await message.reply_message("Wait a moment...")
    try:
        params = {
            'key': GOOGLEAI_KEY,
        }
        json_data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': message.text.split(maxsplit=1)[1],
                        },
                    ],
                },
            ],
        }
        response = await fetch.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            params=params,
            json=json_data,
            timeout=20.0,
        )
        if not response.json().get("candidates"):
            return
        await msg.edit_message(html.escape(response.json()["candidates"][0]["content"]["parts"][0]["text"]))
    except Exception as e:
        print(e)



app.start()
idle()
