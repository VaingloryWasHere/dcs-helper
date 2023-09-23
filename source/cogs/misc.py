import discord
from discord import app_commands
from discord.ext import commands
import confuse

class Bot(commands.GroupCog):
 	def __init__(self,bot):
 		self.bot = bot



 	@app_commands.command(name='version',description="Get version information")
 	async def version(self, interaction: discord.Interaction):
 		config = confuse.Configuration('DCS Helper', __name__)
 		config.set_file('config.yaml')

 		ver = config['Version'].get()
 		ver_full = config['Version Meta'].get()
 		instance = config['Instance'].get()

 		em = discord.Embed(title="Version Query.",description=" ",color=discord.Color.red())
 		em.add_field(name=f" - Version:",value=f"{ver}",inline=True)
 		em.add_field(name=f"   Version Meta:",value=f"{ver_full}",inline=True)
 		em.add_field(name=f" - Instance:",value=f"{instance}",inline=False)

 		chlog = ""
 		listch = config['Changelog'].get()
 		for element in listch:
 			element = str(element)
 			chlog = f"{chlog}\n - {element}" if element == listch[0] else f"{chlog}\n- {element}"
 			print(chlog)

 		em.add_field(name=f" - Changelog:",value=f"{chlog}",inline=False)

 		await interaction.response.send_message(embed=em)