import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading

bot_token = os.environ.get("TOKEN", "5785101195:AAHbWMBDku6q9tWJdMIJtJvhEl3ajmC0spQ") 
api_hash = os.environ.get("HASH", "dfebf9cc52b859771cf8a1d447e751a5") 
api_id = os.environ.get("ID", 12916125 )
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = os.environ.get("STRING", "BQBy9cUwAOv6tGCX1Rea0p8T5fiFXi2PedK8rJGfRF2Kub7R_5rc6xdvqxqc83iSNWDQ-tYWwrew8HeHfqm5uPrjZ8Yp7VrwXjOhBlgtTBjh1YL-SPauU20n8YLFvZKl4lnF5i-mhEE-tmhB8mFAERljaI6O5jjhvFs8B43z1KxmlYvCHxlYlG62betGPpnzpFn322FRcrR4BAgHps-ODPYpaNQIYpvXK0ncd_nbEh2dOJc48pX0OtdTZ4T6lqQb2ecwNOvUSdnAN79eHtZFJwRrzG1haLpUqNMie7iOy5UhS7EuwDJwuyF4RLasiaxsfa_W1uCjwbDnvl6JW1-_MtOrYnOlYQA")
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# upload status
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# progress writter
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot, I can send you restricted content by it's post link__",
	reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]]), reply_to_message_id=message.id)


@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# joining chats
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
				return
			bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
		except UserAlreadyParticipant:
			bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
		except InviteHashExpired:
			bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)
	
	# getting message
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		msgid = int(datas[-1].split("?")[0])

		# private
		if "https://t.me/c/" in message.text:
			chatid = int("-100" + datas[-2])
			if acc is None:
				bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
				return
			try: handle_private(message,chatid,msgid)
			except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
		
		# public
		else:
			username = datas[-2]
			msg  = bot.get_messages(username,msgid)
			try: bot.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id)
			except:
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
	

# handle private
def handle_private(message,chatid,msgid):
		msg  = acc.get_messages(chatid,msgid)

		if "text" in str(msg):
			bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
			return

		smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')

		upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		upsta.start()
		
		if "Document" in str(msg):
			try:
				thumb = acc.download_media(msg.document.thumbs[0].file_id)
			except: thumb = None
			
			bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
			if thumb != None: os.remove(thumb)

		elif "Video" in str(msg):
			try: 
				thumb = acc.download_media(msg.video.thumbs[0].file_id)
			except: thumb = None

			bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
			if thumb != None: os.remove(thumb)

		elif "Animation" in str(msg):
			bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
			   
		elif "Sticker" in str(msg):
			bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

		elif "Voice" in str(msg):
			bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

		elif "Audio" in str(msg):
			try:
				thumb = acc.download_media(msg.audio.thumbs[0].file_id)
			except: thumb = None
				
			bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
			if thumb != None: os.remove(thumb)

		elif "Photo" in str(msg):
			bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

		os.remove(file)
		if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		bot.delete_messages(message.chat.id,[smsg.id])


# infinty polling
bot.run()
