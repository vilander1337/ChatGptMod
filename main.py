import os
import requests
import openai
import json 

from base.module import command, BaseModule
from pyrogram.types import Message

class ChatGptMod(BaseModule):
    @command("chatgpt")
    async def chatcmd(self, _, message: Message):
        noq = self.S["errors"]["noquestion"]
        unk = self.S["errors"]["unknown"]

        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply(noq)
                return
            user_text = args[1]
            model = "text-davinci-003"
            temperature = 0.7
            max_tokens = 512
            completions = openai.Completion.create(
                engine=model,
                prompt=user_text,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
            chatgpt_text = completions.choices[0].text.strip()
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
            openai.api_key = user_key
            await message.reply(kadd)
        except Exception as e:
            await message.reply(f"{unk} <b>{str(e)}</b>")



    