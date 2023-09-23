from tinydb import TinyDB, Query, where
import discord
from discord import app_commands
from discord.ext import commands
from .currency import Bank, ShopManager

currency = Bank()

class Basic(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.bank = Bank()


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



#SHOP COG.
class Shop(commands.GroupCog):
  def __init__(self,bot):
    self.bot = bot
    self.prices = {
    'static1':100,
    'static2':200,
    'static3':300,
    'beyondlimit':500,
    'activitygodring':1000
    }

  @app_commands.command()
  async def view(self,interaction: discord.Interaction, page: int = 1):
    match page:
      case 1:
        await interaction.response.send_message(embed = await ShopManager.get_page_one())
      case 2:
        await interaction.response.send_message(embed = await ShopManager.get_page_two())
      case _:
        await interaction.response.send_message("Unknown page number!")

  @app_commands.command()
  async def buy(self,interaction: discord.Interaction, item_id: str):
    shopm = ShopManager()    
    await interaction.response.defer()
    if item_id != 'activitygodring' or 'vainrevenge':

      res,userbal = await shopm.activateBooster(interaction, item_id,self.prices)
      match res:
        case True:
          em = discord.Embed(title="Success!",description=f"Booster with id `{item_id}` was bought.",color=discord.Color.blue())
          em.add_field(name="New Balance:",value=f"{userbal} Gold Coins.")
          await interaction.edit_original_response(embed=em)
        case False:
          await interaction.edit_original_response(content="You're too poor dumbo.")
        case "unknown":
          await interaction.edit_original_response(content="...?")

    else:
      await shopm.activateSpecial(item_id)