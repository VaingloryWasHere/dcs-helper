from tinydb import TinyDB, Query, where
from discord import app_commands
from discord.ext import commands
import discord
bank = TinyDB("../data/bank.json")

class Bank:

  @staticmethod
  def create_account(owner_id,patronbool): #not actually a bool...json won't accept it.

    if isinstance(bank.get(where('id') == owner_id), dict): #dict returned, user entry already exists.
      return

    #else....

    bank.insert({'id': owner_id, 'gold coins': 0, 'patron':patronbool})
    print(f"Account created for user id {owner_id} with balance 0")

  @staticmethod
  def get_balance(owner_id): 
    user = Query()
    res = bank.get(user.id==owner_id)
    final_amount = res['gold coins']
    return final_amount

  @staticmethod
  def update_balance(owner_id, amount: int, operation: str):
    if operation == "add":
      print("Starting add operation..")
      target = Query()
      targetAccount = bank.get(target.id==owner_id)
      previousBalance = targetAccount['gold coins']
      print(f"previous bal of {owner_id} is {previousBalance}. Adding {amount}")
      targetAffect = Query()
      bank.update({'gold coins': previousBalance + amount}, targetAffect.id==owner_id)
      print(f"Success. New balance: {previousBalance+amount}")
    
      
    elif operation == "subtract":
      target = Query()
      targetAccount = bank.get(target.id==owner_id)
      previousBalance = targetAccount['gold coins']
      targetAffect = Query()
      bank.update({'gold coins': previousBalance - amount}, targetAffect.id==owner_id)

    else:
      print("unknown error")
      return

class Economy(commands.Cog):
  def __init__(self,bot):
    self.bot = bot


  @app_commands.command(name='balance',description='Get the amount of coins you have.')
  async def balance(self,interaction: discord.Interaction):
    try:
      bal = Bank.get_balance(interaction.user.id)
      embed = discord.Embed(title="Your balance.", description = f"You currently have {bal} Gold Coins", colour = discord.Colour.green())
      await interaction.response.send_message(embed=embed)
      
    except TypeError:

      await interaction.response.send_message("Looks like ya don't have an account yet Worry not! I just created one for ya.")
      Bank.create_account(interaction.user.id,"False")


  @app_commands.command()
  async def shop(self,interaction: discord.Interaction):
      from cogs.boosters import Boosters as boosters
      em = boosters.getshopembed(interaction)
      await interaction.response.send_message(embed=em)


  @app_commands.command()
  async def buy(self,interaction: discord.Interaction, itemid: str):
      res = await boosters.activate(interaction,itemid)
      if res == False:
          await interaction.response.send_message("You're too poor to afford that.")
      elif res == "unknown":
          await interaction.response.send_message("That's not a real item.")
      else:
          await interaction.response.send_message("it worked... i think.")


  @app_commands.command(name="addgold")
  async def addgold(self, interaction: discord.Interaction,amt: int):
      Bank.update_balance(interaction.user.id,amt,'add')

  
