import time
import json
import hashlib
import os
import datetime
import asyncio
import sys
from functools import reduce

import discord
from discord.ext import tasks

from messagegen import MessageGenConfig, MessageGen

# BOTのトークン
BOT_TOKEN=os.getenv('NARIKIRI_BOT_TOKEN')

# ループ間隔 デフォルトは30分
LOOP_INTERVAL = os.getenv('NARIKIRI_LOOP_INTERVAL', 1800)


class MainClient(discord.Client):
    def __init__(self, messagegen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messagegen = messagegen


    async def setup_hook(self) -> None:
        self.background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    @tasks.loop(seconds=LOOP_INTERVAL)
    async def background_task(self):
        pass

    @background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author == self.user:
            return

        if message.mention_everyone:
            return
        
        if self.user in message.mentions:
            question_message = message.content.replace("<@" + str(self.user.id) + ">","")

            print("質問メッセージ：" + question_message)

            reply_message = self.messagegen.reply_gen(question_message, [])

            print("回答メッセージ："+reply_message)

            await message.channel.send(reply_message)

            return
        


        return

def main():
    # 起動時引数からキャラクターキーを取得
    args = sys.argv
    if len(args) <=1:
        print("usage: python main.py (character_key)")
        return

    character_key = args[1]

    # JSON形式のファイル読み込み
    with open("config/common_cfg.json", 'r', encoding="utf-8") as f:
        config = json.load(f)

    target_character = {}
    valid_key = False

    for character in config['characters']:
        # もしキャラクターキーもしくは
        if character_key == character['key'] or character_key in character['alias']:
            target_character = character
            valid_key = True

    if not valid_key:
        print("invalid character_key error")
        return

    # openai起動
    with open("prompt/"+target_character['key']+ ".txt", 'r', encoding="utf-8") as f:
        prompt = f.read()

    messagegen = MessageGen(MessageGenConfig(), prompt)


    its = discord.Intents.default()
    its.message_content = True
    client = MainClient(messagegen, intents=its)
    client.run(BOT_TOKEN)




if __name__ == "__main__":
    main()
