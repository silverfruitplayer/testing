import html
#from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import choice
from pyrogram import Client, filters, idle
from aiohttp import ClientSession
#from json import loads
from httpx import AsyncClient, Timeout
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

app = Client("geminiai", bot_token="5808857616:AAElBa0KAWMe-YF9c34hBh0ydTTlihA_hrE", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")


session = ClientSession()
session.close()

fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")

@app.on_message((filters.text) & filters.command("image"))
async def gemini_chatbot(_, message):
    if len(message.command) == 1:
        return await message.reply_text("Ask a question.")
    if not GOOGLEAI_KEY:
        return await message.reply_text("GOOGLEAI_KEY env is missing!!!")    
    if message.text.split(None, 1)[1]:
        message_text = message.text.strip().replace("/ask","",1).strip()
    if filters.text:
        message_text = message.text    
    msg = await message.reply_text("Wait a moment...")
    try:
        params = {
            'key': GOOGLEAI_KEY,
        }
        json_data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': f"{message_text}\n",
                        },
                    ],
                },
            ],
        }
        response = await fetch.post(
            'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateImage',
            params=params,
            json=json_data,
            timeout=20.0,
        )
        if not response.json().get("candidates"):
            return await msg.edit_text("Your question contains slang or foul languages that has been blocked for security reasons.")
        await msg.reply_photo(html.escape(response.json()["candidates"][0]["content"]["parts"][0]["text"]))
    except Exception as e:
        print(e)

@app.on_message((filters.text) & filters.command("image"))
async def gemini_chatbot(_, message):
    if len(message.command) == 1:
        return await message.reply_text("Ask a question.")
    if not GOOGLEAI_KEY:
        return await message.reply_text("GOOGLEAI_KEY is missing!!!")    
    if message.text.split(None, 1)[1]:
        message_text = message.text.strip().replace("/image","",1).strip()
    if filters.text:
        message_text = message.text    
    msg = await message.reply_text("Wait a moment...")
    body = {
        "prompt": message_text,
        "image_context": {
            "crop_and_resize": {
                "size": {
                    "height": 512,
                    "width": 512
                }
            }
        }
    }

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GOOGLEAI_KEY}",
    }

    # Make the request
    response = requests.post(endpoint, json=body, headers=headers)
    response.raise_for_status()

    # The API returns "image_bytes" as base64 encoded string
    #image_bytes = response.json()["candidates"][0]["image_bytes"]

    print response.json()

    if not response.json().get("candidates"):
        return await msg.edit_text("Your question contains slang or foul languages that has been blocked for security reasons.")

    await message.reply_photo(image_bytes)
app.start()
idle()
