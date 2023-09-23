from tinydb import TinyDB, Query, where
from discord import app_commands
from discord.ext import commands
import discord

shop = {}

shop['static1'] = {
  'id':'static1',
  'name':'Static Booster: Tier 1',
  'price':100,
  'description':'Adds 1 xp to the random xp given per message.'
}

shop['static2'] = {
  'id': 'static2',
  'name':'Static Booster: Tier 2.',
  'price':200,
  'description':'Adds 2 xp to the random xp given per message.'
}

shop['static3'] = {
  'id':'static3',
  'name':'Static Booster: Tier 3.',
  'price': 300,
  'description':'Adds 3 xp to the random xp given per message.'
}

class Bank:
  def __init__(self):
    self.bank = TinyDB("../data/bank.json")

  def create_account(self,owner_id,strbool): #not actually a bool...json won't accept it.

    if isinstance(self.bank.get(where('id') == owner_id), dict): #dict returned, user entry already exists.
      return

    #else....

    self.bank.insert({'id': owner_id, 'gold coins': 0, 'patron':bool(strbool)})
    print(f"Account created for user id {owner_id} with balance 0")

  @staticmethod
  def get_balance(self,owner_id): 
    res = self.bank.get(where(user.id)==owner_id)
    final_amount = res['gold coins']
    return final_amount

  @staticmethod
  def update_balance(self,owner_id, amount: int, operation: str):
    if operation == "add":
      print("Starting add operation..")
      targetAccount = self.bank.get(where('id')==owner_id)
      previousBalance = targetAccount['gold coins']
      self.bank.update({'gold coins': previousBalance + amount}, where('id')==owner_id)
    
      
    elif operation == "subtract":
      targetAccount = self.bank.get(where('id')==owner_id)
      previousBalance = targetAccount['gold coins']
      targetAccount['gold coins'] = previousBalance - amount
      self.bank.update(targetAccount, where('id')==owner_id)

    else:
      print("unknown error")
      return


class ShopManager: 
  def __init__(self):
    self.xp = TinyDB("../data/xp.json")
    self.bank = Bank()

  async def get_page_one(self):
    em = discord.Embed(title="DCS: Gold Store",description="**__Page One: Boosters \nPage Two: Special Items.__**",color=discord.Color.green())
    em.add_field(name="Static Booster: Tier 1",value="Price: 100 Gold Coins\nEffect: Adds one extra xp per message.\nDuration: 1000 messages. \nID: `static1`",inline=False)
    em.add_field(name="Static Booster: Tier 2",value="Price: 200 Gold Coins\nEffect: Adds two extra xp per message.\nDuration: 1000 messages. \nID: `static2`",inline=False)
    em.add_field(name="Static Booster: Tier 3",value="Price: 300 Gold Coins\nEffect: Adds three extra xp per message.\nDuration: 1000 messages \nID: `static3`.",inline=False)
    em.add_field(name="Beyond Limit Booster",value="Price: 500 Gold Coins\nEffect: Increases earnable xp by 100%.\nDuration: 1000 messages. \nID:`beyondlimit`",inline=False)
    em.set_footer(text="None of the boosters stack. Use `/shop buy <item id>` to buy.")
    return em

  async def get_page_two(self):
    em = discord.Embed(title="DCS: Gold Store",description="Page One: Boosters \nPage Two: Special Items.",color=discord.Color.green())
    em.add_field(name="Activity God's Ring",value="Stolen from the God of Activity Fiablo himself.\nCost: 1000 Gold Coins\nEffect:Earn half of the xp you need to reach the next level. \nID: `activitygodring`",inline=False)
    em.set_footer(text="Diamond store coming soon for Patrons Use `/shop buy <item_id>` to buy..")
    return em

  async def activateBooster(self, interaction,boosterID,prices):
    userid = interaction.user.id
    userbal = self.bank.get_balance(userid)
    userdata = self.xp.get(Query().id==userid)

    match boosterID:
      case "static1":
        if userbal > prices['static1']:
          self.bank.update_balance(userid,100,"subtract")
          userdata['booster'] = {'id':'static1','duration':1000}
        else:
          return False, userbal

      case "static2":
        if userbal > prices['static2']:
          self.bank.update_balance(userid,200,"subtract")
          userdata['booster'] = {'id': 'static2','duration':1000}
        else:
          return False, userbal

      case "static3":
        if userbal > prices['static3']:
          self.bank.update_balance(userid,300,"subtract")
          userdata['booster'] = {'id': 'static3','duration':1000}
        else:
          return False, userbal

      case _:
        return "unknown", userbal

    self.xp.update(userdata,Query().id==userid)
    print("booster purchase successful.")
    return True, userbal - prices[boosterID]




class BoosterHandler():
  def __init__(self):
    self.xp = "../data/xp.json"
    self.bank = Bank()

  @staticmethod
  def getshopembed(interaction):
    embed = discord.Embed(title="Shop.",description="Plenty of items for everyone!",colour=discord.Colour.green())
    for entry in shop:
      item = shop[entry]
      embed.add_field(name=f"{item['name']}",value=f"{item['description']} \n Price: {str(item['price'])} Gold Coins.",inline=False)

    player_balance = currency.get_balance(interaction.user.id)
    embed.add_field(name="Your balance:",value=f'{player_balance} Gold Coins.')

    embed.set_footer(text=f"{interaction.user.name}",icon_url=interaction.user.display_avatar)

    return embed

  @staticmethod
  async def activate(interaction,boosterID):
    userid = interaction.user.id
    userbal = self.bank.get_balance(userid)
    userdata = self.xp.get(Query().id==userid)

    match boosterID:
      case "static1":
        if userbal > static_one['price']:
          self.bank.update_balance(userid,100,"subtract")
          userdata['booster'] = "static1"

        else:
          return False

      case "static2":
        if userbal > static_two['price']:
          self.bank.update_balance(userid,200,"subtract")
          userdata['booster'] = "static2"

        else:
          return False

      case "static3":
        if userbal > static_three['price']:
          self.bank.update_balance(userid,300,"subtract")
          userdata['booster'] = "static3"

        else:
          return False

      case _:
        return "unknown" 

    self.xp.update(userdata,Query().id==userid)
    print("booster purchase successful.")
    return True








