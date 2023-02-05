import pyrogram	
from pyrogram import Client, filters, idle
from pyrogram.types import *
from pyrogram import enums
import datetime
import pymongo
from pymongo import MongoClient
import math
from math import *
import time

client = MongoClient("mongodb+srv://really651:K4vSnRMEsZhqsTqS@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Productsdb"]
collection = db["coll"]

app = Client(
"uploadbot1",
api_id = 11855414,
api_hash = "71449899c824b5bc9a91d8a52b20c5f3",
bot_token = "5624770835:AAEyK318nLW7PlVGWsezEYYNnBgCNJL4P40"
)

help = """<u>    ⚪HELP SECTION</u>

<b>👌As mentioned already this bot is used to get restricted content from Public Telegram Channel! You don\'t have to worry about file size this bot can send upto 4GB file🤩 And also its fastest than any other bots. its better if you see yourself😎

🔍To Get Restricted Content, Just send the link of the message🔍

🤨However there is limit while sending video and documents. but thats not bad and there is no limit with other contents✨

🛠 If you get bug/issues report us @Developerschat 👥</b>
"""

key = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🌀Project Channel", url="t.me/DevelopersPage"), InlineKeyboardButton(text ="⚙️Support Group", url = "t.me/developerschat")],
[InlineKeyboardButton(text ="🤔 Help 🗞", callback_data ="help"), InlineKeyboardButton(text ="✍️ Developer 🔍", user_id = 1365625365)]
])

back = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🔙Back", callback_data ="back")]
])

@app.on_callback_query()
async def ans(client, callback):
	if callback.data =="help":
		await app.edit_message_text(callback.message.chat.id, callback.message.id, help, reply_markup = back, parse_mode = enums.ParseMode.HTML)
	if callback.data =="back":
		await app.edit_message_text(callback.message.chat.id, callback.message.id, f"👋Hello {callback.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel! Even upto 4GB file!</b>\n\n✍️Just Send me the link of the message🤩", parse_mode = enums.ParseMode.HTML, reply_markup = key)

async def checking(client, message):
	try:
		a = await app.get_chat_member("@channel", message.from_user.id).status 
		return True 
	except:
		return False

@app.on_message(filters.command("start"))
async def strf(client, message):
		await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel! Even upto 4GB file!</b>\n\n✍️Just Send me the link of the message🤩", parse_mode = enums.ParseMode.HTML, reply_markup = key)

async def send(client, message):
	now = datetime.datetime.now()
	chat_id = message.chat.id 
	user = collection.find_one({'user_id': chat_id})
	s = str(message.text[13:])
	m = s.split("/")[0]
	s1 = f"@{m}"
	m1 = s.split("/")[1]
	a = await app.get_messages(s1, int(m1))
	try:
		if a.photo:
			await app.send_photo(message.chat.id, a.photo.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.document:
			text =""
			size = float(a.document.file_size/1024/1024)
			flor = math.floor(size)
			text+=f"{flor}"
			text+=f"MB"
			collection.update_one({'user_id': chat_id}, {'$set': {'bonus_time': now}})
			i2 = await message.reply("🤩Don\'t rush dude! Just only 5 seconds⌚")
			time.sleep(5)
			await app.send_document(message.chat.id, a.document.file_id, caption = a.caption)		
			await app.delete_messages(message.chat.id, i2.id)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.poll:
			await message.reply("🤨For Now I Don\'t Support Poll!")
			return 
		if a.video:
			collection.update_one({'user_id': chat_id}, {'$set': {'bonus_time': now}})
			i1 = await message.reply("🤩Don\'t rush dude! Just only 5 seconds⌚")
			time.sleep(5)
			await app.send_video(message.chat.id, a.video.file_id, caption = message.caption)
			await app.delete_messages(message.chat.id, i1.id)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.text:
			await message.reply(a.text)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Text! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return
		if a.audio:
			await app.send_audio(message.chat.id, a.audio.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
		if a.voice:
			await app.send_voice(message.chat.id, a.voice.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
		else:
			await message.reply("⚠️Either i don\'t know this type of content! or I couldn't save it.")			
	except Exception as e:
		await message.reply("🔰Oppss! Make sure that the channel is public and the link is starts with <b>https://</b>", parse_mode = enums.ParseMode.HTML)	

@app.on_message()
async def down(client, message):
	chat_id = message.chat.id 
	now = datetime.datetime.now()
	user = collection.find_one({'user_id': chat_id})
	if user and 'bonus_time' in user:
		bonus_time = user['bonus_time']
		if now - bonus_time < datetime.timedelta(minutes=1):
			await app.send_message(chat_id, '⌚You have to wait 1 minute in order to send another task! 😏Don\'t disturb me!😊')
			return 			
		else:
			await send(client, message)
	else:
		await send(client, message)


print("Successful")
app.run()
