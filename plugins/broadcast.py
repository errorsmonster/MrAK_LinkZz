import datetime, time, os, asyncio,logging 
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton
from utils import broadcast_messages, broadcast_messages_group
from pyrogram import Client, filters, enums
from database.users_chats_db import db
from info import ADMINS
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text('Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs...')
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss:\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await bot.send_message(message.chat.id, f"Bʀᴏᴀᴅᴄᴀsᴛ Coᴍᴩʟᴇᴛᴇᴅ:\nTɪᴍᴇ Tᴀᴋᴇᴅ{time_taken} Sᴇᴄ\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ: {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSucᴄᴇꜱꜱ: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages To Groups...'
    )
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for group in groups:
        pti, sh = await broadcast_messages_group(int(group['id']), b_msg)
        if pti:
            success += 1
        elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Groups {total_groups}\nCompleted: {done} / {total_groups}\nSuccess: {success}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Groups {total_groups}\nCompleted: {done} / {total_groups}\nSuccess: {success}")

        
