import os

import discord
from discord.ext import commands
import yaml

import json

intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

prefix = 'drinks/'

# crappy config setup
with open('config-prod.yaml') as config:
    CONFIG = yaml.safe_load(config)


@bot.slash_command(name="add_drink", guild_ids=list(CONFIG['guild_ids']))
async def add_drink(ctx: discord.interactions, user: discord.User):
    dt = get_guild_drink_tracker(ctx.guild_id)
    add(dt, user.name, "drink")
    write(dt, ctx.guild_id)
    await ctx.respond(f"Added drink for {user}".format(user=user.name))


@bot.slash_command(name="add_chug", guild_ids=list(CONFIG['guild_ids']))
async def add_chug(ctx: discord.interactions, user: discord.User):
    dt = get_guild_drink_tracker(ctx.guild_id)
    add(dt, user.name, "chug")
    write(dt, ctx.guild_id)
    await ctx.respond(f"Added chug for {user}".format(user=user.name))


@bot.slash_command(name="add_shot", guild_ids=list(CONFIG['guild_ids']))
async def add_shot(ctx: discord.interactions, user: discord.User):
    dt = get_guild_drink_tracker(ctx.guild_id)
    add(dt, user.name, "shot")
    write(dt, ctx.guild_id)
    await ctx.respond(f"Added shot for {user}".format(user=user.name))


def add(drink_tracker: dict, username: str, drink_type: str):
    if drink_tracker.get(username):
        drink_tracker[username][drink_type] += 1
    else:
        drink_tracker[username] = {"chug": 0, "shot": 0, "drink": 0}
        drink_tracker[username][drink_type] += 1


@bot.slash_command(name="clear_all_drinks", guild_ids=list(CONFIG['guild_ids']))
async def clear_all_drinks(ctx: discord.interactions):
    dt = get_guild_drink_tracker(ctx.guild_id)
    dt.clear()
    write(dt, ctx.guild_id)
    await ctx.respond("All drinks, chugs, and shots for each user is removed")


@bot.slash_command(name="clear_user_drinks", guild_ids=CONFIG['guild_ids'])
async def clear_user_drinks(ctx: discord.interactions, user: discord.User):
    dt = get_guild_drink_tracker(ctx.guild_id)
    if dt.get(user.name):
        del dt[user.name]
        write(dt, ctx.guild_id)
        await ctx.respond(f"Removed all drinks, chugs, and shots for {user}".format(user=user.name))
    else:
        await ctx.respond(f"Cannot be cleared because {user} is a coward with no drinks".format(user=user.name))


@bot.slash_command(name="display_all_drinks", guild_ids=list(CONFIG['guild_ids']))
async def display_all_drinks(ctx: discord.interactions):
    dt = get_guild_drink_tracker(ctx.guild_id)
    if dt == {}:
        await ctx.respond("Imagine not having anyone on the board")
    else:
        await ctx.respond(embed=format_output(dt))


@bot.slash_command(name="display_user_drinks", guild_ids=list(CONFIG['guild_ids']))
async def display_user_drinks(ctx: discord.interactions, user: discord.User):
    dt = get_guild_drink_tracker(ctx.guild_id)
    if dt.get(user.name):
        await ctx.respond(embed=format_output({user.name: dt[user.name]}))
    else:
        await ctx.respond(f"{user} is a coward with no drinks".format(user=user.name))


def get_guild_drink_tracker(guild_id: discord.Guild.id):
    try:
        with open(prefix + str(guild_id) + ".json") as json_file:
            return json.load(json_file)
    except Exception as err:
        print(err)
        return {}


def format_output(drinks: dict):
    res = discord.Embed(title="Take a Drink Chart", colour=discord.Colour.green())
    for key, value in drinks.items():
        row = f"> Chugs: {value['chug']}\n> Shots: {value['shot']}\n> Drinks: {value['drink']}"
        res.add_field(name=key, value=row)
    return res


def write(drink_tracker: dict, guild_id: discord.Guild.id):
    with open(prefix + str(guild_id) + ".json", "w") as file:
        file.write(json.dumps(drink_tracker))


if not os.path.exists(os.path.dirname(prefix)):
    os.mkdir(prefix)

bot.run(CONFIG['token'])
