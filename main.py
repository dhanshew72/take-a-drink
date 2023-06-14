import discord
from discord.ext import commands
import yaml

# local db setup
DRINK_TRACKER = {}


intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

# crappy config setup
with open('config-prod.yaml') as config:
    CONFIG = yaml.safe_load(config)


@bot.slash_command(name="add_drink", guild_ids=CONFIG['guild_ids'])
async def add_drink(ctx: discord.interactions, user: discord.User):
    add(user.name, "drink")
    await ctx.respond(f"Added drink for {user}".format(user=user.name))


@bot.slash_command(name="add_chug", guild_ids=CONFIG['guild_ids'])
async def add_chug(ctx: discord.interactions, user: discord.User):
    add(user.name, "chug")
    await ctx.respond(f"Added chug for {user}".format(user=user.name))


@bot.slash_command(name="add_shot", guild_ids=CONFIG['guild_ids'])
async def add_shot(ctx: discord.interactions, user: discord.User):
    add(user.name, "shot")
    await ctx.respond(f"Added shot for {user}".format(user=user.name))


def add(username: str, drink_type: str):
    if DRINK_TRACKER.get(username):
        DRINK_TRACKER[username][drink_type] += 1
    else:
        DRINK_TRACKER[username] = {"chug": 0, "shot": 0, "drink": 0}
        DRINK_TRACKER[username][drink_type] += 1


@bot.slash_command(name="clear_all_drinks", guild_ids=CONFIG['guild_ids'])
async def clear_all_drinks(ctx: discord.interactions):
    DRINK_TRACKER.clear()
    await ctx.respond("All drinks, chugs, and shots for each user is removed")


@bot.slash_command(name="clear_user_drinks", guild_ids=CONFIG['guild_ids'])
async def clear_user_drinks(ctx: discord.interactions, user: discord.User):
    if DRINK_TRACKER.get(user.name):
        del DRINK_TRACKER[user.name]
        await ctx.respond(f"Removed all drinks, chugs, and shots for {user}".format(user=user.name))
    else:
        await ctx.respond(f"Cannot be cleared because {user} is a coward with no drinks".format(user=user.name))


@bot.slash_command(name="display_all_drinks", guild_ids=CONFIG['guild_ids'])
async def display_all_drinks(ctx: discord.interactions):
    if DRINK_TRACKER == {}:
        await ctx.respond("Imagine not having anyone on the board")
    else:
        await ctx.respond(DRINK_TRACKER)


@bot.slash_command(name="display_user_drinks", guild_ids=CONFIG['guild_ids'])
async def display_user_drinks(ctx: discord.interactions, user: discord.User):
    if DRINK_TRACKER.get(user.name):
        await ctx.respond(user.name + " drinks: " + str(DRINK_TRACKER[user.name]))
    else:
        await ctx.respond(f"{user} is a coward with no drinks".format(user=user.name))


bot.run(CONFIG['token'])
