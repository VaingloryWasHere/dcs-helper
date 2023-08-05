import AO3
import discord
from discord import app_commands
from discord.ext import commands


class Ao3(commands.GroupCog, group_name='ao3'):
	def __init__(self,bot):
		self.bot = bot
		print("[INFO] Cog Ao3 initialized succesfully.")

	@app_commands.command(name='work',description="Find basic information about an ao3 work.")
	async def work(self,interaction: discord.Interaction, url: str):
		#defer the interaction so we can take our sweet time doing the math.
		await interaction.response.defer()

		workid = AO3.utils.workid_from_url(url)
		print(f"Work ID: {workid}")
		work = AO3.Work(workid)
		em = discord.Embed(title=f"WorkID: {workid}",description=f"Chapters: {work.nchapters}\nKudos:{work.kudos}",color=discord.Color.blue())			
		await interaction.followup.send(embed=em)

	@app_commands.command(name='user',description="Find basic information about an ao3 user.")
	async def user(self, interaction: discord.Interaction, username: str):
		user = AO3.User(username)
		#making the embed.
		embed=discord.Embed(title=f"User Query: {username}",description=f"User URL: {user.url}\nUser's Bio: {user.bio}\nWorks published: {user.works}",color=discord.Color.red())
		embed.set_footer(text="Build by discord user apostle_of_vanity")
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name='kudos',description="Get a free kudos!")
	async def kudos(self, interaction: discord.Interaction, workurl: str):
		try:
			await interaction.response.defer()
			workid = AO3.utils.workid_from_url(workurl)
			session = AO3.GuestSession()
			work = AO3.Work(workid, load_chapters=False, session=session)
			print(work.kudos)
			work.leave_kudos()
			await interaction.followup.send("Successfully gave you a kudos!")
			work.reload()
			print(work.kudos)
		except Exception as e:
			if isinstance(Exception, AO3.utils.UnexpectedResponseError):
				await interaction.followup.send(f"Hey! You've already left kudos on that work! No cheating!")
			else:
				await interaction.followup.send(f"Error: ```{e}```")






