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

@app.on_message(filters.command("start"))
async def strf(client, message):
		await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel and Group</b>.\n\n✍️Send /save to save restricted content✨", parse_mode = enums.ParseMode.HTML)

async def send(client, message):
	s = str(message.text[13:])
	m = s.split("/")[0]
	s1 = f"@{m}"
	m1 = s.split("/")[1]
	a = await app.get_messages(s1, int(m1))	
	if a.photo:
		await app.send_photo(message.chat.id, a.photo.file_id, caption = message.caption)
		await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
	if a.document:		
		text =""
		size = float(a.document.file_size/1024/1024)
		flor = math.floor(size)
		text+=f"{flor}"
		text+=f"MB"
		collection.update_one({'user_id': chat_id}, {'$set': {'bonus_time': now}})
		i2 = await message.reply("🤩Don\'t rush dude! Just only 5 seconds⌚")
		time.sleep(5)
		await app.send_document(message.chat.id, a.document.file_id, caption = f"{a.caption}\n\n💾File Size: {text}")
		await app.delete_messages(message.chat.id, i2.id)
		await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
	if a.poll:
		await message.reply("🤨For Now I Don\'t Support Poll!")
	if a.video:
		collection.update_one({'user_id': chat_id}, {'$set': {'bonus_time': now}})
		i1 = await message.reply("🤩Don\'t rush dude! Just only 5 seconds⌚")
		time.sleep(5)
		await app.send_video(message.chat.id, a.video.file_id, caption = message.caption)
		await app.delete_messages(message.chat.id, i1.id)
		await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
	if a.text:
		await message.reply(a.text)
		await message.reply("<b>🔥Hurray! I\'ve successfully saved your Text! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)

@app.on_message(filters.command("start"))
async def strf(client, message):
		await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel and Group</b>.\n\n✍️Send /save to save restricted content✨", parse_mode = enums.ParseMode.HTML)

@app.on_message()
async def down(client, message):
	chat_id = message.chat.id 
	now = datetime.datetime.now()
	user = collection.find_one({'user_id': chat_id})
	if user and 'bonus_time' in user:
		bonus_time = user['bonus_time']
		if now - bonus_time < datetime.timedelta(minutes=1):
			await app.send_message(chat_id, '🙂You have to wait 1 minute in order to send another task! 😏Don\'t disturb me!😊')
			return
		else:
			send(client, message)
	else:
		send(client, message)


print("Successful")
app.run()
