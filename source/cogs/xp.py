from tinydb import TinyDB, Query, where
import discord
import random
from discord.ext import commands
import confuse
from discord import app_commands
from DiscordLevelingCard import Settings, RankCard

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())


config_file = confuse.Configuration('MyGreatApp', __name__)
# Add config items from specified file. Relative path values within the
# file are resolved relative to the application's configuration directory.
config_file.set_file('config.yaml')
class XPManager:

# Python code to read config.txt
    @staticmethod
    def read_config_file():
        configvars = ['Print XP Given']
        config = {}
        for configvar in configvars:
            config[configvar] = config_file[configvar].get(bool)

        return config

    @staticmethod
    async def getname(id):
      person = await bot.get_user(id)
      return person.name

    @staticmethod
    def checkexist(id):
        db = TinyDB("../data/xp.json")
        entries = db.all()
        for entry in entries:
            if entry['id'] == id:
                db.close()
                return True
        db.close()
        return False 

    @staticmethod
    def createEntry(id):
        if XPManager.checkexist(id):
            return False
        else:
            db = TinyDB("../data/xp.json")
            entry = {
                "id": id,
                "xp": 0,
                "level": 0,
                "next_level": 1,
                "threshold": 100,
                "booster": None
            }
            db.insert(entry)
            print("Entry created.")
            db.close()
            return True

      
    @staticmethod
    async def checkrankup(id):
      db = TinyDB(r"../data/xp.json")
      if db == None:
        print("DB is NoneType. returning false.")
        return False
      else:
        entry = db.get(where('id') == id)
        next_level = entry['level'] + 1
        threshold = next_level * 100

        print(f"next_level is {next_level}")
        print(f"threshold is {threshold}")
        
        if entry["xp"] >= threshold: #threshold passed or reached.
          print(f'''User whose current level is {entry["level"]} and who's xp({entry["xp"]} has reache the threshold for the next level, level {next_level}, which is {threshold} will now be ranked up. Returning true. ''')
          entry["level"] = next_level #next level is current level
          entry['next_level'] = next_level + 1
          entry['threshold'] = entry['next_level'] * 100
          entry['xp'] = 0


          meh = Query()
          db.update(entry,meh.id==id)

        meh = Query()
        db.update(entry,meh.id==id)
        db.close()

    @staticmethod
    def givexp(id,rangee): #range is a list btw.
        db = TinyDB("../data/xp.json")
        
        user = db.get(where('id') == id) #fetch entry matching user's id.
        prev_xp = user['xp'] #get previous xp
        print(f"prev xp: {prev_xp}")

        modifier = user['booster'] #get modifier.

        xp = random.randint(rangee[0],rangee[1]) #Get a random integer between range(inclusive) 1-10 for standard msgs and 1-3 for small message.
        

        if user['xp'] == 0:
              user['xp'] = 1 #set xp to one if its zero.
              print("xp set to 1")
              meh = Query()
              db.update(user,meh.id == id)
              return True
            
        else:
            match modifier: #match statement introduced in python 3.10

                case "static1": #adds 1 xp to random xp.
                    xp = xp + 1


                    user['xp'] = prev_xp + xp
                    print("static1 used")

                case "static2": #adds 2 xp to random xp.
                    xp = xp + 2
                    user['xp'] = prev_xp + xp
                    print("static2 used")

                case "static3":
                    xp = xp + 3
                    user['xp'] = prev_xp + xp
                    print("static3 used")


                case _:

                    user['xp'] = prev_xp + xp



            meh2 = Query()
            db.update(user,meh2.id == id)
            db.close()
            settings = XPManager.read_config_file()
            if settings['Print XP Given'] == "True":
                print(f"XP Given: {xp}. Booster: {user['booster']}")

    @staticmethod
    def getinfo(id):
        db = TinyDB("../data/xp.json")
        user = db.get(where("id") == id)

        if user == None: 
            errorembed = discord.Embed(title="You haven't send a message yet!",description="How about getting your name registered in the bot's database by sending a message first?",color=discord.Colour.red())
            return errorembed

        returnlist = [user.get("xp", 0), user.get("level", 0), user.get("next_level", 0), user.get("totalxp", 0)]
        db.close()
        return returnlist

    @staticmethod
    def getdb():
        db = TinyDB('../data/xp.json')
        return db

    @staticmethod
    def fixprofile(id):
        db = XPManager.getdb()
        buggedprofile = db.get(where('id') == id)
        fixedprofile = buggedprofile

        if not buggedprofile:
            print("Profile in fixprofile() returned none.")

        elif buggedprofile:
            fixedprofile['next_level'] = buggedprofile['level'] + 1 #set fixed profile's next-level to bugged profile's level + 1
            fixedprofile['threshold'] = fixedprofile['next_level'] * 100 #next_level: 3, threshold = 300  
            db.update(fixedprofile, Query().id == id)
            print("profile fixed!")


class XP(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        await self.bot.process_commands(message)
        
        if isinstance(message.channel, discord.DMChannel):
            return  # Exclude DM messages from XP tracking
            
        msg_len = len(message.content.split())
        XPManager.createEntry(message.author.id)
        
        if msg_len > 4:
            XPManager.givexp(message.author.id, [1, 10]) #for msgs greater than 4 words, give 1-10 xp.
        else:
            print("short msg xp.")
            XPManager.givexp(message.author.id, [1, 3]) #for 4 words or less, give 1 to 3 xp.
        
        await XPManager.checkrankup(message.author.id)

    @app_commands.command(name="rank",description="See your rank.")
    async def rank(self,interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()

        XPManager.fixprofile(interaction.user.id)#just in case the entry is missing some stuff.
        XPManager.fixprofile(member)

        if member:
            userinfo = XPManager.getinfo(member.id)
            avatar_url = member.display_avatar.url
        else:
            userinfo = XPManager.getinfo(interaction.user.id)
            avatar_url = interaction.user.display_avatar.url

        if isinstance(userinfo, discord.Embed):
            await interaction.followup.send(embed=userinfo)
            return #the user's name wasn't in xp.json. userinfo is actually an error embed now.


        card_settings = Settings(
        background="rezero.jpg",
        text_color="white",
        bar_color="white"
    )

        a = RankCard(
            settings=card_settings,
            avatar=avatar_url,
            level=userinfo[1],
            current_exp=userinfo[0],
            max_exp=userinfo[2] * 100,
            username=f"{interaction.user.name if not member else member.name}"
        )
        print(a.username)
        image = await a.card2(resize=100)
        await interaction.edit_original_response(attachments=[discord.File(image, filename="rank.png")]) # providing filename is very importan



                
