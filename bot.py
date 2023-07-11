import pyrogram	
from pyrogram import Client, filters, idle
from pyrogram.types import *
from pyrogram import enums
import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Productsdb"]
collection = db["coll"]

app = Client(
"uploaderbot",
api_id = 11855414,
api_hash = "71449899c824b5bc9a91d8a52b20c5f3",
bot_token = "5624770835:AAGEUrV9kMXHHq8-VTjS_3Oeobnr9hsmRsM"
)

help = """<u>    ⚪HELP SECTION</u>

<b>👌As mentioned already this bot is used to get restricted content from Public Telegram Channel! You don\'t have to worry about file size this bot can send upto 4GB file🤩 And also its fastest than any other bots. its better if you see yourself😎

🔍To Get Restricted Content, Just send the link of the message🔍

🤨However there is limit while sending video and documents. but thats not bad and there is no limit with other contents✨

🛠 If you get bug/issues report us @Neuralg 👥</b>
"""

key = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🌀Project Channel", url="t.me/Neuralp"), InlineKeyboardButton(text ="⚙️Support Group", url = "t.me/Neuralg")],
[InlineKeyboardButton(text ="🤔 Help 🗞", callback_data ="help"), InlineKeyboardButton(text ="✍️ Developer 🔍", user_id = 1365625365)]
])

back = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🔙Back", callback_data ="back")]
])


#adding inline download or saving option 
@app.on_inline_query()
async def inline(c , q):
    query = q.query 
    sp = query.split("/")
    mid = sp[-1]
    chan = sp[-2]
    print (query , chan , mid)  
    a = await app.get_messages(chan , int(mid))
    if a.photo:
        await q.answer( results = [
        ( InlineQueryResultCachedPhoto(
        photo_file_id=a.photo.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/developerspage")]])
    ))])
    
    if a.document:				
        await q.answer( results = [
        ( InlineQueryResultCachedDocument(
        document_file_id=a.document.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/developerspage")]])
    ))])
		
    if a.video:						
        await q.answer( results = [
        ( InlineQueryResultCachedVideo(
        video_file_id = a.video.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/developerspage")]])
    ))])
    if a.text:
        await q.answer( results = [ ( InlineQueryResultArticle(
        title = " Restricted content ",
        description ="text message ",
        input_message_content = InputTextMessageContent(a.text) ,
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join us🤗", url="https://t.me/developerspage")]])
		    ))])
    if a.audio:
        await q.answer( results = [
        ( InlineQueryResultCachedAudio(
        audio_file_id=a.audio.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/developerspage")]])
    ))])
    if a.voice:
        await q.answer( results = [
        ( InlineQueryResultCachedVoice(
        voice_file_id=a.voice.file_id,
        title = "Restricted Content",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/developerspage")]])
    ))])
    else :
        await q.answer( results = [ ( InlineQueryResultArticle(
        title = " Link Required ",
        description ="Pls provide public channel or group link",
        input_message_content = InputTextMessageContent("**need help 🤔**\nstart the bot in private") ,
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join us🤗", url="https://t.me/developerspage")]])
		    ))])
 
    
	
@app.on_callback_query()
async def ans(client, callback):
	if callback.data =="help":
		await app.edit_message_text(callback.message.chat.id, callback.message.id, help, reply_markup = back, parse_mode = enums.ParseMode.HTML)
	if callback.data =="back":
		await app.edit_message_text(callback.message.chat.id, callback.message.id, f"👋Hello {callback.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel! Even upto 4GB file!</b>\n\n✍️Just Send me the link of the message🤩", parse_mode = enums.ParseMode.HTML, reply_markup = key)

async def checking(client, message):
	try:
		a = await app.get_chat_member("@neuralp", message.from_user.id)
		return True 
	except Exception as e:
		#await message.reply(e)
		return False

@app.on_message(filters.command("start"))
async def strf(client, message):
		chat_id = message.chat.id 
		user = collection.find_one({"user_id": chat_id})
		if user:
			await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel! Even upto 4GB file!</b>\n\n✍️Just Send me the link of the message🤩", parse_mode = enums.ParseMode.HTML, reply_markup = key)
		else:
			collection.insert_one({"user_id": chat_id})
			await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Save Restricted Messages bot. This bot can help you to save restricted content from <b>public channel! Even upto 4GB file!</b>\n\n✍️Just Send me the link of the message🤩", parse_mode = enums.ParseMode.HTML, reply_markup = key)

join = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🔂Join The Channel", url="t.me/Neuralp")]
])

@app.on_message(filters.regex("http"))
async def send(client, message):
	check = await checking(client, message)
	if check == True:
		pass	 
	else:
		await message.reply("⚠️Dude in order to use this bot you must be a member of our channel!\nJoin and try again♻️", reply_markup = join)
		return
	try:
		s = str(message.text[13:])
		m = s.split("/")[0]
		s1 = f"@{m}"
		m1 = s.split("/")[1]
		a = await app.get_messages(s1, int(m1))	
		if a.photo:
			await app.send_photo(message.chat.id, a.photo.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.document:				
			await app.send_document(message.chat.id, a.document.file_id, caption = a.caption)	
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.poll:
			await message.reply("🤨For Now I Don\'t Support Poll!")
			return 
		if a.video:						
			await app.send_video(message.chat.id, a.video.file_id, caption = message.caption)			
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.text:
			await message.reply(a.text)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Text! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return
		if a.audio:
			await app.send_audio(message.chat.id, a.audio.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		if a.voice:
			await app.send_voice(message.chat.id, a.voice.file_id, caption = message.caption)
			await message.reply("<b>🔥Hurray! I\'ve successfully saved your Media! Enjoy🤩</b>", parse_mode = enums.ParseMode.HTML)
			return 
		else:
			await message.reply("⚠️Either i don\'t know this type of content! or I couldn't save it.")
	except Exception as e:
		await message.reply("🔰Oppss! Make sure that the channel is public and the link is starts with <b>https://</b>", parse_mode = enums.ParseMode.HTML)	
	

print("Successful")
app.run()
