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
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from io import BytesIO

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

credentials_url = 'https://lodabsdk.s3.ap-southeast-1.amazonaws.com/credentials.json?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiEAv7dwl02NNhLF%2BL%2FHDpmEb7DSSBIIxnwT0UpVo0387HgCIAodstNBqGHHhc5ItI8N3pePTrIp0WdMokPrmVJMZMWYKu0CCJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzQ0MDgyOTUwMzIwIgz6k77FPWIM3V47FVkqwQJLOBtb7B8fScNSm1XSq3nDLmqJKKn2AetA0I9hRm6A4Qu7TtzqvYc209qKgJqHfIT%2BBp0SegMttmLFreBw5WGsZve8KNh4HNgblYFTSpV5%2Fx8ZmesXynnaeYTVO%2FNKuh%2B1x3Apq%2FR50c3zaxoJooIK1gB3oClRcORAgCnZvHEYKoE6bCRjLY%2B8ym%2BXL%2FTdrm8NH3L6QZWkfkvMYhedGB0IRoTMO8HjLhi%2BJrlqoI%2BJFC3Dh8SGXHEDMGw2JGIwNGO007bYxyuiMgxgJFW7ege60tfee7ArGjo0S6jbF%2FUBRl70AVaBOvXfjOLYRuaGAAB9Gn0SbB17Iss3rTsW4Btpwrjv3%2FIsLKmfsX5pPe0rE0pQwrHbyGUsuPLGyH91LFag%2BxG%2BlCyRiYnqam%2BWqeDlTv8e0qGQrZfdSMJTuqNVDPgw6Y7KrQY6swKgJw6nD9Z49ccLehd85nLT96J34hmT14gX0O6b5IbhdRrXoKUOuU%2Bsx9gktR2p5L6OPpk2EtBP8c61bfZzQhgHWC0gHGO8XZ035xqqcxN49GzNG3WovsJVHD4wfk1uA8dsZcoa%2BKUukEy538mTRzHRhSW8jPtaz6DsQE06fIgcj6hA2TOXsewlxdIlRzV%2FIhEHw7tUKfa1ZPUQN3nMi1R9roFkMbbIWGbcMtlUSUHgEvJh1RVgqXlNgv297cQkeukpJ1dVLOl3UB1OGDVOF%2BxwA%2BddhbAW4EZcWyRW04TOfei%2B3loASsRbdT5MIPoUFBK32zaNPAi7CSqH5%2FV9E4PFBJqz16oIRl%2B30hHSSQKwbltPWYI4ltpaQHCzMQjNJZ3dW9lDIFkcHlEzRofertpoA6JJ&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240125T161513Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAVAHHRFCYFYETVDMZ%2F20240125%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Signature=66586cc2e214a3f461706442e255ff0a2c88cc347fd8fc15376c37461ae17b07'
response = requests.get(credentials_url)
credentials_content = BytesIO(response.content)

# Google Cloud Vision API client
client = vision.ImageAnnotatorClient.from_service_account_file(credentials_content)

@app.on_message(filters.command("analyze"))
async def analyze_image(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        # Get the photo with the highest resolution
        photo = message.reply_to_message.photo[-1]
        file_id = photo.file_id
        file_info = app.get_file(file_id)

        # Download the photo
        photo_path = file_info.download()

        # Analyze the image using Google Cloud Vision API
        with open(photo_path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]

        # Send the labels back to the user
        if labels:
            labels_text = "\n".join(labels)
            await message.reply_text(f"Labels detected:\n{labels_text}")
        else:
            await message.reply_text("No labels detected.")
    else:
        message.reply_text("Please reply to an image for analysis.")



@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(f"Hi {message.from_user.mention}, Ask any question to start over.\nYou can search images too (NSFW content not allowed)")


@app.on_message(filters.command("ask"))
async def gemini_chatbot(_, message):
    if len(message.command) == 1:
        return await message.reply_text("Please ask a question")
    if not GOOGLEAI_KEY:
        return await message.reply_text("GOOGLEAI_KEY env is missing!!!")
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
            return await msg.edit_text("Your question contains slang or foul languages that has been blocked for security reasons.")
        await msg.edit_text(html.escape(response.json()["candidates"][0]["content"]["parts"][0]["text"]))
    except Exception as e:
        print(e)



app.start()
idle()
