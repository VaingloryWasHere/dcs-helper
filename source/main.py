import discord
from discord.ext import commands
import os
from tinydb import TinyDB, Query, where
from discord import app_commands
from datetime import *
import confuse
from DiscordLevelingCard import Settings, RankCard

from cogs.verify import Verifier
from cogs.alive import keep_alive
from cogs.xp import XP, Leaderboard
from cogs.economy import Basic, Shop
from cogs.ao3 import Ao3
from cogs.misc import Bot



bot = commands.Bot(command_prefix = ",",intents=discord.Intents.all())

#initialisation stuff

@bot.event
async def on_ready():
    print("Bot is currently online!")
    await bot.add_cog(Verifier(bot))
    await bot.add_cog(Basic(bot))
    await bot.add_cog(Shop(bot))
    await bot.add_cog(Ao3(bot))
    await bot.add_cog(Leaderboard(bot))
    await bot.add_cog(XP(bot))
    await bot.add_cog(Bot(bot))
    #add commands to a group

@bot.command()
async def avatar(ctx):
    filename = "../assets/avatar.jpg"
    await ctx.author.display_avatar.save(filename)
    file = discord.File(fp=filename)
    await ctx.send("Enjoy :>", file=file)


@bot.command(name="sync")
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 718710286596702220:
        await bot.tree.sync()

        em = discord.Embed(title="Syncing in progress.",description="Fetching slash command list.",colour=discord.Colour.blue())
        emSend= await ctx.send(embed=em)

    for slash_command in bot.tree.walk_commands():
        em.add_field(name=slash_command.name, 
                     value=slash_command.description if slash_command.description else slash_command.name, 
                     inline=False) 
                     # fallbacks to the command name incase command description is not defined

        await emSend.edit(embed=em)
        
    else:
        await ctx.send('You must be the owner to use this command!')


keep_alive()

TOKEN = "MTExNTk5MzcxNjEzNDUxODg3NQ.GPtq7_.ucSRcMszvTCLHxhomLeheGyCFqXD1K4woTyytw"

bot.run(TOKEN)