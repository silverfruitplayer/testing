import html
from random import choice
from pyrogram import Client, filters, idle
from aiohttp import ClientSession
from httpx import AsyncClient, Timeout
import asyncio
import requests
import logging
import os
from google.cloud import vision_v1
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

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


@app.on_message(filters.text)
async def gemini_chatbot(_, message):
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
                            'text': message.text,
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


vision_api_key = "AIzaSyA4DY9qLKEosHtJBpKMVRUDBrnCYkbLevc"

vision_client = vision_v1.ImageAnnotatorClient(credentials=vision_v1.Credentials.from_authorized_user_info(api_key=vision_api_key))



@app.on_message(filters.photo & filters.sticker)
async def handle_photo(client, message):
    # Download the photo from Telegram
    photo_path = await message.download()

    # Open the photo as a file-like object
    with io.open(photo_path, "rb") as image_file:
        content = image_file.read()

    # Construct the request to the Vision API
    image = vision_v1.Image(content=content)
    requests = [
        {
            "image": image,
            "features": [
                {
                    "type": vision_v1.Feature.Type.IMAGE_PROPERTIES,
                }
            ],
        }
    ]

    # Make the request to the Vision API
    response = vision_client.batch_annotate_images(requests=requests)

    # Get the image properties from the response
    image_properties = response[0].image_properties_annotation

    # Construct the response message to send to Telegram
    response_message = ""

    # Get the dominant colors from the image
    dominant_colors = image_properties.dominant_colors.colors
    for color in dominant_colors:
        response_message += f"Dominant color: {color.color.red}, {color.color.green}, {color.color.blue}\n"

    # Get the image's average color
    average_color = image_properties.dominant_colors.average_color
    response_message += f"Average color: {average_color.red}, {average_color.green}, {average_color.blue}\n"

    # Send the response message to Telegram
    await message.reply_text(response_message)

    # Delete the downloaded photo
    os.remove(photo_path)




app.start()
idle()
