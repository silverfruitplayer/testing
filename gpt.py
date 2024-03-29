import html
from random import choice
from pyrogram import Client, filters, idle, enums
from aiohttp import ClientSession
from httpx import AsyncClient, Timeout
import asyncio
import requests
import logging
import os
import os
#import PIL.Image
from PIL import Image
import google.generativeai as genai

GOOGLEAI_KEY = "AIzaSyC2cKZRxUsoCfYaveyab08QEp7jxsRWrJk"

genai.configure(api_key=GOOGLEAI_KEY)

DOWNLOAD = "./DownLoads"
model = genai.GenerativeModel("gemini-pro-vision")
model1 = genai.GenerativeModel('gemini-pro')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("hmmm", bot_token="5808857616:AAHOGP2XmsIiP2OiQAbBa2i-UOW_Rh099JY", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")


#session = ClientSession()
#session.close()

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


@app.on_message(filters.sticker | filters.photo)
async def say(_, message):
    try:
        x = await message.reply_text("Please Wait...")
        if message.sticker:
            file_path = await message.download(DOWNLOAD)
            files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
            response0 = model.generate_content(files)
            await message.reply_photo(files)
            await x.edit_text(
                f"**Details Of Sticker You Provided:** {response0.parts[0].text}", parse_mode=enums.ParseMode.MARKDOWN
            )    
            os.remove(file_path)
        else:
            if message.photo:
                y = message.reply_to_message
                base_img = await message.download()
                img = Image.open(base_img)
                if y and y.text:
                    response = model.generate_content([f"{message.reply_to_message.text}"],img)
                    await x.edit_text( 
                        f"**You Asked {y}**\n\n** And Details Of Photo You Provided:** {response.parts[0].text}", parse_mode=enums.ParseMode.MARKDOWN
                    )
                else:
                    response = model.generate_content(img)
                    await x.edit_text( 
                        f"**Details Of Photo You Provided (Because you have not provided Any Caption so providing the explaination Please Reply With Some Question To Generate):**\n\n{response.parts[0].text}", parse_mode=enums.ParseMode.MARKDOWN
                    )                    
                os.remove(base_img)
    except Exception as e:
        print(e)

@app.on_message(filters.text)
async def gemini_chatbot(_, message):
    if not GOOGLEAI_KEY:
        return await message.reply_text("GOOGLEAI_KEY env is missing!!!")
    if message.reply_to_message:
        return
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
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            params=params,
            json=json_data,
            timeout=20.0,
        )
        if not response.json().get("candidates"):
            return await msg.edit_text("Your question contains slang or foul languages that has been blocked for security reasons.")
            
        char = {html.escape(response.json()['candidates'][0]['content']['parts'][0]['text'])}
        
        if len(char) > 4096:
            filename = "Answer.txt"
            
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(evaluation.strip()))
                await app.send_document(
                    message.chat.id,
                    document=filename,
                    caption=f"Here is your Answer For question {message.text}",
                    disable_notification=True,
                )
                os.remove(filename)
        
        await msg.edit_text(
            f"**Your Question was:**\n{message.text}\n\n**Your Answer is:**\n{char}"
        )    
    except Exception as e:
        print(e)


app.start()
idle()
