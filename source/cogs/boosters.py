from tinydb import TinyDB, Query, where
import discord
from discord import app_commands
from cogs.currency import Bank

currency = Bank()

xp = TinyDB("../data/xp.json")


static_one = {
	'id':'static1',
	'name':'Static Booster: Tier 1',
	'price':100,
	'description':'Adds 1 xp to the random xp given per message.'
}

static_two = {
	'id': 'static2',
	'name':'Static Booster: Tier 2.',
	'price':200,
	'description':'Adds 2 xp to the random xp given per message.'
}

static_three = {
	'id':'static3',
	'name':'Static Booster: Tier 3.',
	'price': 300,
	'description':'Adds 3 xp to the random xp given per message.'
}

shop = {}

shop['static1'] = static_one
shop['static2'] = static_two
shop['static3'] = static_three

class Boosters():

	@staticmethod
	def getshopembed(interaction):
		embed = discord.Embed(title="Shop.",description='Boosters are the only items available.',colour=discord.Colour.green())
		for entry in shop:
			item = shop[entry]
			embed.add_field(name=f"{item['name']}",value=f"{item['description']} \n Price: {str(item['price'])} Gold Coins.")

		player_balance = currency.get_balance(interaction.user.id)
		embed.add_field(name="Your balance:",value=f'{player_balance} Gold Coins.')

		embed.set_footer(text=f"{interaction.user.name}",icon_url=interaction.user.display_avatar)

		return embed

	@staticmethod
	async def activate(interaction,boosterID):
		userid = interaction.user.id
		userbal = currency.get_balance(userid)
		userdata = xp.get(Query().id==userid)

		match boosterID:
			case "static1":
				if userbal > static_one['price']:
					currency.update_balance(userid,100,"subtract")
					userdata['booster'] = "static1"

				else:
					return False

			case "static2":
				if userbal > static_two['price']:
					currency.update_balance(userid,200,"subtract")
					userdata['booster'] = "static2"

				else:
					return False

			case "static3":
				if userbal > static_three['price']:
					currency.update_balance(userid,300,"subtract")
					userdata['booster'] = "static3"

				else:
					return False

			case _:
				return "unknown" 

		xp.update(userdata,Query().id==userid)
		print("booster purchase successful.")
		return True