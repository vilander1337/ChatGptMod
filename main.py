import os
import requests
import openai
import json 

from base.module import command, BaseModule
from .db import Base, Keys
from pyrogram.types import Message
from sqlalchemy import select


class ChatGptMod(BaseModule):
    @property
    def db_meta(self):
        return Base.metadata
    
    @command("chatgpt")
    async def chatcmd(self, _, message: Message):
        noq = self.S["errors"]["noquestion"]
        unk = self.S["errors"]["unknown"]

        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply(noq)
                return
            async with self.db.session_maker() as session:
                db_key = await session.scalar(select(Keys).filter_by(user_id=message.from_user.id))
            print(db_key.oaikey)
            openai.api_key = db_key.oaikey
            user_text = args[1]
            completions = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature = 0.7,
                max_tokens = 512,
                messages=[{"role": "assistant", "content": user_text}]
            )
            chatgpt_text = completions.choices[0].message.content
            await message.reply_text(chatgpt_text)
        except Exception as e:
            await message.reply(f"{unk} <b>{str(e)}</b>")

    @command("key")
    async def keysys(self, _, message: Message):
        kadd = self.S["key"]["keyadded"]
        nkey = self.S["key"]["nokey"]
        unk = self.S["errors"]["unknown"]

        try:
            arg = message.text.split()
            if len(arg) < 2:
                await message.reply(nkey)
                return
            user_key = arg[1]
            async with self.db.session_maker() as session:
                db_key = await session.scalar(select(Keys).filter_by(user_id=message.from_user.id))
                db_key = Keys(user_id=message.from_user.id, oaikey=user_key)
                session.add(db_key)
                await session.commit()
            await message.reply(kadd)
        except Exception as e:
            await message.reply(f"{unk} <b>{str(e)}</b>")
    