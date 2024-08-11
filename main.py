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
# BOT_TOKEN=os.getenv('NARIKIRI_BOT_TOKEN')

# ループ間隔 デフォルトは30分
LOOP_INTERVAL = os.getenv('NARIKIRI_LOOP_INTERVAL', 1800)

# 設定ファイル読込


def load_file(file_path):
    fp = open(file_path, 'r', encoding="utf-8")

    data = json.load(fp)

    fp.close()

    return data


class MainClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        return


def main():
    # its = discord.Intents.default()
    # its.message_content = True
    # client = MainClient(intents=its)
    # client.run(BOT_TOKEN)
    # openai起動
    with open("prompt/default.txt", 'r', encoding="utf-8") as f:
        prompt = f.read()

    messagegen = MessageGen(MessageGenConfig(), prompt)



if __name__ == "__main__":
    main()
