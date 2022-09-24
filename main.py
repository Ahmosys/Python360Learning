import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from modules import scrapper

load_dotenv()
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game("./ahmosys#6967")
    )

@client.command(name="timetable", alias=["edt", "schedule"], description="Retrieve the timetable of the current week.")
@commands.cooldown(1, 15, commands.BucketType.user)
async def get_timetable(ctx: commands.Context):
    driver, driver_wait = scrapper.init()
    message = await ctx.send("```**Attempt to login to SSO of 360Learning...**```")
    scrapper.login(driver=driver)
    await message.edit(content="```**Switch from homepage to timetable page...**```")
    scrapper.get_timetable_page(driver=driver, driver_wait=driver_wait)
    await message.edit(content="```**Generating the screenshot...**```")
    scrapper.get_screenshot(driver=driver)
    await message.delete()
    await ctx.send(file=discord.File("edt.png"))
    

client.run(os.getenv("DISCORD_TOKEN"))