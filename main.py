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
        status=discord.Status.online,
        activity=discord.Game("For any issues ./ahmosys#6967"),
    )


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Mmmmmmh, I have the impression that this command does not exist."
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions to do this command.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oops, you cannot use this command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"This command is on cooldown. Please wait {error.retry_after:.2f}s"
        )


@client.command(
    name="timetable",
    alias=["edt", "schedule"],
    description="Retrieve the timetable of the current week.",
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def get_timetable(ctx, *, date: str = None):
    driver, driver_wait = scrapper.init()
    message = await ctx.send("**Attempt to login to SSO of 360Learning...**")
    scrapper.login(driver=driver)
    await message.edit(
        content="""
**Attempt to login to SSO of 360Learning :white_check_mark:**
**Switch from homepage to timetable page...**
    """
    )
    scrapper.get_timetable_page(driver=driver, driver_wait=driver_wait, date_value=date)
    await message.edit(
        content="""
**Attempt to login to SSO of 360Learning :white_check_mark:**
**Switch from homepage to timetable page :white_check_mark:**
**Generating the screenshot...**
    """
    )
    date_start_week, date_end_week = scrapper.get_date_week(driver=driver)
    scrapper.get_screenshot(driver=driver)
    await message.edit(
        content="""
**Attempt to login to SSO of 360Learning :white_check_mark:**
**Switch from homepage to timetable page :white_check_mark:**
**Generating the screenshot :white_check_mark:**
    """
    )
    await message.delete(delay=2)
    file = discord.File("timetable.png")
    em = discord.Embed(
        title=":date: Timetable", description=f"From *{date_start_week}* to *{date_end_week}*.", timestamp=ctx.message.created_at, color=0x5570FE
    )
    em.set_image(url="attachment://timetable.png")
    em.set_footer(text=ctx.author)
    await ctx.send(embed=em, file=file)


client.run(os.getenv("DISCORD_TOKEN"))
