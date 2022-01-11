import discord
from asyncio import sleep
from discord.ext import commands
import collections


bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())

story = []
started = False
queue = collections.deque([])
storychannel = 0
TOKEN = ""


@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game(name=f"Creating stories....."))


@bot.event
async def on_message(msg):
    global queue, storychannel
    if (
        msg.channel.id == storychannel
        and len(story) != 200
        and not msg.content.startswith("-")
        and started
    ):

        current = queue[0]
        if current == msg.author.id:
            queue.rotate(-1)
            next_ = queue[0] if queue else "no-one"

            story.append(f"{msg.content}. ")

            await msg.channel.send(f"<@{next_}>, it's your turn.")

    await bot.process_commands(msg)


@bot.command()
async def end(ctx):
    global story, started, queue
    embed = discord.Embed(
        title="Are you sure you want to end the story?",
        description=f"To end the story, please react below. If {round(len(queue)/2)} people have reacted, the story will end. This will timeout in 10 seconds.",
        color=0xFFA500,
    )
    embed.set_footer(
        text=f"Command invoked by {ctx.author} | Bot by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    msg = await ctx.send(embed=embed)
    started = False
    await msg.add_reaction("✅")
    await sleep(10)
    cache_msg = discord.utils.get(bot.cached_messages, id=msg.id)

    if (cache_msg.reactions[0].count) >= len(queue) / 2:
        await ctx.channel.purge(limit=100000)
        await sleep(2)
        await ctx.send("The story has ended.")
        queue = collections.deque([])
        await ctx.send("".join(story))
        story = []

    else:
        await ctx.send("Enough people didn't react, continuing the story.")
        started = True


@bot.event
async def on_reaction_add(reaction, user):
    if (
        user != bot.user
        and reaction.emoji == "☑️"
        and reaction.message.id == reactionmsgid
        and not started
    ):
        queue.append(user.id)


@bot.command()
async def start(ctx):
    global started, reactionmsgid, queue, storychannel
    storychannel = ctx.channel.id
    queue = collections.deque([])
    embed = discord.Embed(
        title="Story Time!",
        description="A new story is starting in 10 seconds! React below to enter :)",
        color=0xFFA500,
    )
    embed.set_footer(
        text=f"Command invoked by {ctx.author} | Bot by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("☑️")
    reactionmsgid = msg.id

    await sleep(10)
    if len(queue) < 2:
        await ctx.send("Not enough people to start the story.")
        queue = collections.deque([])
        started = False
    await ctx.channel.send(f"The story is starting! <@{queue[0]}> is first!")
    started = True


@bot.command()
async def source_code(ctx):
    e = discord.Embed(
        title="Source Code",
        description="You can find my source code [here](https://github.com/SockYeh/StoryBot) ",
        color=0xFFA500,
    )
    e.set_footer(
        text=f"Command invoked by {ctx.author} | Bot by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=e)


bot.run(TOKEN)
