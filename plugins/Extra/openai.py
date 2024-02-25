from pyrogram import Client, filters
from info import OPENAI_API, LOG_CHANNEL
import openai
import asyncio

openai.api_key = OPENAI_API

async def send_message_in_chunks(client, chat_id, text):
    max_length = 4096  # Maximum length of a message
    for i in range(0, len(text), max_length):
        await client.send_message(chat_id, text[i:i+max_length])


@Client.on_message(filters.command("ask"))
async def ask_question(client, message):
        user_id = message.from_user.id
        if user_id:
            try:
                s = await message.reply_text("ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
                text = message.text.split(" ", 1)[1]
                user_id = message.from_user.id
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=1200,  # Increase the value of max_tokens to allow for longer responses
                    temperature=0.6
                )          
                ai_response = response.choices[0].message.content.strip()
                await s.delete()
                await send_message_in_chunks(client, message.chat.id, f"Hᴇʏ: {message.from_user.mention}\n\nQᴜᴇꜱᴛɪᴏɴ: {text}\n\nAɴꜱᴡᴇʀ:\n\n{response.choices[0].message.content}")
                await send_message_in_chunks(client, LOG_CHANNEL, f"#openai {message.from_user.mention} Avec ID utilisɑteuɾ - {user_id}.\n🔍 M'ɑ pose‌ cette question...👇\n\n🔻 Question: {text}\n\n🔻 Voici lɑ ɾe‌ponse que j’ɑi donne‌e:\n🖍️ {ai_response}\n\n\n🔻 Identifiɑnt :- {user_id} \n🔻 Nom d’utilisɑteuɾ :- {message.from_user.mention}")
                
            except Exception as error:
                print(error)
                await message.reply_text(f"Give any input question like /ask hi")
                await s.delete()