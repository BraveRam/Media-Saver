import pyrogram	
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyromod import listen
from pyrogram import enums
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://really651:K4vSnRMEsZhqsTqS@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Products"]
collection = db["coll"]

api_id = 11855414
api_hash = "71449899c824b5bc9a91d8a52b20c5f3"
bot_token = "5624770835:AAEyK318nLW7PlVGWsezEYYNnBgCNJL4P40-Q"
app = Client(
  "MediaSaver",
  api_id=api_id,
  api_hash=api_hash,
  bot_token=bot_token
)

b = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🖥Developer🖥", user_id = 1365625365)]
]
)

@app.on_message(filters.command("dev") & filters.private)
async def dev(cilent, message):
	await app.send_message(message.from_user.id, "👨‍💻Bot Developer👨‍💻", reply_markup = b)

@app.on_message(filters.command("start") & filters.private)
async def sft(cilent, message):
	ids = message.from_user.id
	users= collection.find_one({"user_id": ids})
	if users:
		await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel and Group</b>.\n\n✍️Send /save to save restricted content✨", parse_mode = enums.ParseMode.HTML)
	else:
		collection.insert_one({"user_id": ids})
		await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel and Group</b>.\n\n✍️Send /save to save restricted content✨", parse_mode = enums.ParseMode.HTML)

@app.on_message(filters.command("save") & filters.private)
async def start(client, message):
    chat_id = message.chat.id 
    now = datetime.datetime.now()
    user = collection.find_one({'user_id': chat_id})
    if user and 'bonus_time' in user:
        bonus_time = user['bonus_time']
        if now - bonus_time < datetime.timedelta(minutes=10):
            await app.send_message(chat_id, '🙂You have to wait 10 minutes in order to send another task!')
            return
        else:
            collection.update_one({'user_id': chat_id}, {'$set': {'bonus_time': now}})
            pass
            #bot.send_message(chat_id, 'You have successfully received your bonus')
    else:
        collection.insert_one({'user_id': chat_id, 'bonus_time': now})
        pass
        #bot.send_message(chat_id, 'You have successfully received your bonus')
   ask = await message.chat.ask("🌀Enter a link that i'll save it's content.\n🚫To Cancel send /cancel.")
   if ask.text =="/cancel": 
   	await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Media Saver bot. This bot can help you to save restricted content from <b>public channel and Group</b>.\n\n✍️Send /save to save restricted content✨", parse_mode = enums.ParseMode.HTML)
   	return 
   else:
   	pass   	
   if "/" in message.text:  	
   	try:
   		s = str(ask.text[13:])
   		m = s.split("/")[0]
   		s1 = f"@{m}" 		
   		m1 = s.split("/")[1]
   		a = await app.get_messages(s1, int(m1))   		   			
   		if a.audio:
   			d = a.audio.file_id			
   			f = a.audio.file_name
   			det = await message.reply("♻️Wait a moment...")
   			c = await app.download_media(d)
   			await app.send_audio(message.chat.id, c, file_name = f)
   			await app.delete_messages(message.from_user.id, det.id)
   			return 
   		if a.poll:
   			await message.reply("🙁For Now I don\'t Save Quiz & Poll!")
   			return 
   		if a.text:
   			await message.reply(a.text)
   		elif a.video:			
   			d = a.video.file_id
   			cap = a.caption
   			f = a.video.file_name
   			det = await message.reply("♻️Wait a moment...")
   			c = await app.download_media(d)
   			await app.send_video(message.chat.id, c, caption = cap, file_name = f)
   			await app.delete_messages(message.from_user.id, det.id)
   		elif a.photo:
   			d = a.photo.file_id
   			cap = a.caption
   			det1 = await message.reply("♻️Wait a moment...")
   			c = await app.download_media(d)
   			await app.send_photo(message.chat.id, c, caption = cap)
   			await app.delete_messages(message.from_user.id, det1.id)
   		elif a.document:			
   			d = a.document.file_id
   			cap = a.caption
   			f = a.document.file_name
   			#file = await app.get_file(d)
#   			print(f"{file.size / 1024 / 1024}")
   			det2 = await message.reply("♻️Wait a moment...")
   			c = await app.download_media(d)
   			await app.send_document(message.chat.id, c, caption = cap, file_name = f)
   			await app.delete_messages(message.from_user.id, det2.id)
   		else:
   			await message.reply("⚠️Either i don\'t know this type of conent! or I couldn't save it.")
   	except Exception as e:
   		await message.reply("🔰Oppss! Make sure that the channel is public and the link is starts with <b>https://</b>", parse_mode = enums.ParseMode.HTML)

      
print("Started")   
app.run()   


