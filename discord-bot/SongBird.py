"""
Developer : Ashutosh Saxena
Date: 3/10/2020
Description : A simple Discord bot to play songs and send memes to a channel
"""
import os
import random
import shutil
import time
from os import system

import aiohttp
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

TOKEN = "NzYxNjM4NTIxNzMwNzYwNzM0.X3dhJg.Q5WxKd6mzhWYJwHwLhWtff9J5XE"  # Bot Tokken
BOT_PREFIX = "-"  # Bot prefix

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command("help")


@bot.event
async def on_ready():
    """
    Prints Logged in when the Bot is Ready
    """
    print("Logged in as: " + bot.user.name + "\n")


@bot.command(pass_context=True, aliases=["J"])
async def join(ctx):
    """
    To make the bot join the Voice Channel you are in
    """
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.remove(file)

    if voice and voice.is_connected():
        await voice.move_to(channel)

    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
        await ctx.send(f"Hiya!!, SongBird Joined {channel}")


@bot.command(pass_context=True, aliases=["dc"])
async def leave(ctx):
    """
    To make the Bot leave the Voice Channel you are in
    """
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Bai Bai !!, SongBird Left {channel}")

    else:
        print(f"The bot has connected to {channel}\n")
        await ctx.send(f"Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=["p"])
async def play(ctx, url: str):
    """
    Play a Song if none is playing currently, from a Youtube/Spotify Link
    """

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more Queued Song(s)\n")
                Queue.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(
                os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song Completed, Playing the next queued\n")
                print(f"Songs still in Queue : {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")

                time.sleep(1)

                voice.play(discord.FFmpegPCMAudio("song.mp3"),
                           after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.1

            else:
                Queue.clear()
                return
        else:
            Queue.clear()
            print("No Songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            Queue.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but its being played")
        await ctx.send("ERROR: Music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed Old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No Old Queue Folder")

    await ctx.send("Getting everything ready now ")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        "format":
        "bestaudio/best",
        "quite":
        True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading Audio Now\n")
            ydl.download([url])
    except:
        print(
            "FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)"
        )
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"),
               after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print(f"Playing: {nname[0]}\n")


@bot.command(pass_context=True)
async def pause(ctx):
    """
    Pause the Current Song Playing
    """
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Paused")
        voice.pause()
        await ctx.send("Music Paused")
    else:
        print("Music is not playing")
        await ctx.send("Music is not playing")


@bot.command(pass_context=True)
async def resume(ctx):
    """
    Resume if the Current Song is Paused
    """
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Music Resumed")
        voice.resume()
        await ctx.send("Music Resumed")
    else:
        print("Music is not paused")
        await ctx.send("Music is not Paused")


Queue = {}


@bot.command(pass_context=True)
async def add(ctx, url):
    """
    To add a Song to the Queue, from a Youtube/Spotify Link
    """
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in Queue:
            q_num += 1
        else:
            add_queue = False
            Queue[q_num] = q_num

    queue_path = os.path.abspath(
        os.path.realpath("Queue" + f"\song{q_num}.%(ext)s"))

    ydl_opts = {
        "format":
        "bestaudio/best",
        "quite":
        True,
        "outtmpl":
        queue_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    await ctx.send("Getting the Song ready now ")

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading Audio Now\n")
            ydl.download([url])
    except:
        print(
            "FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)"
        )
        q_path = os.path.dirname(os.path.realpath("Queue" + f"\song{q_num}"))
        system(f"spotdl -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Added song to the queue.")
    print("Song added to queue\n")


@bot.command(pass_context=True, aliases=["next"])
async def skip(ctx):
    """
    To Skip the current song playing to the next one if it is there in the Queue
    """

    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.stop()

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more Queued Song(s)\n")
                Queue.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(
                os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song Skipped, Playing the next queued\n")
                print(f"Songs still in Queue : {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")

                time.sleep(1)

                voice.play(discord.FFmpegPCMAudio("song.mp3"),
                           after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.1

            else:
                Queue.clear()
                return
        else:
            Queue.clear()
            print("No Songs were queued before the ending of the last song\n")

    await ctx.send("Song Skipped, Playing the next queued")
    check_queue()


@bot.command(pass_context=True)
async def ping(ctx):
    """
    Send a messsage giving the latency of the Bot
    """
    await ctx.send("Pong! = " + str(round(bot.latency * 1000)) + "ms")


@bot.command(pass_context=True)
async def dank(ctx):
    """
    Posts a Dankmeme from r/Dankmemes
    """
    embed = discord.Embed(title="From r/Dankmemes")

    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                "https://www.reddit.com/r/dankmemes/new.json?sort=hot") as r:
            res = await r.json()
            embed.set_image(url=res["data"]["children"][random.randint(0, 25)]
                            ["data"]["url"])
            await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def meme(ctx):
    """
    Posts a Meme from r/memes
    """
    embed = discord.Embed(title="From r/memes")

    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                "https://www.reddit.com/r/memes/new.json?sort=hot") as r:
            res = await r.json()
            embed.set_image(url=res["data"]["children"][random.randint(0, 25)]
                            ["data"]["url"])
            await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=["h"])
async def help(ctx):
    """
    Sends a embeded message specifing all the commands currently there
    """

    embed = discord.Embed(
        colour=discord.Colour.red(),
        title="--SongBird--",
        description="Bot Prefix is - (dash)\n This is a Simple Discord Bot to send Memes & Play Songs\n ",
    )

    embed.set_author(
        name="Made by : Ashutosh",
        icon_url="https://avatarfiles.alphacoders.com/172/172111.png",
    )
    embed.set_image(
        url="https://initiate.alphacoders.com/images/745/cropped-250-250-745065.png?5477"
    )
    embed.add_field(
        name="join",
        value="Makes the Bot Join the Voice Channel You are in.",
        inline=True,
    )
    embed.add_field(name="leave",
                    value="Gives the Latency of the Bot",
                    inline=True)
    embed.add_field(name="ping",
                    value="Gives the Latency of the Bot",
                    inline=True)
    embed.add_field(name="play",
                    value="The makes the bot play the song",
                    inline=True)
    embed.add_field(name="pause",
                    value="Pauses the current song being played",
                    inline=True)
    embed.add_field(name="resume",
                    value="Resumes if the song is paused",
                    inline=True)
    embed.add_field(name="add",
                    value="Adds a new song to the Queue",
                    inline=True)
    embed.add_field(name="next",
                    value="Skips the current song being played",
                    inline=True)
    embed.add_field(name="meme",
                    value="Posts a meme from r/memes",
                    inline=True)
    embed.add_field(name="dank",
                    value="Posts a meme from r/Dankmemes",
                    inline=True)

    embed.set_footer(text="Made with LOVE")

    await ctx.send(embed=embed)


bot.run(TOKEN)
