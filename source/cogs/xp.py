from tinydb import TinyDB, Query, where
import discord
import random
from discord.ext import commands
import confuse
from discord import app_commands
from DiscordLevelingCard import Settings, RankCard
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

class XPManager:
    def __init__(self,bot):
        self.db = TinyDB(os.environ.get("XP_PATH"))
        self.bot = bot

    async def getname(self,id):
      person = await self.bot.get_user(id)
      return person.name

    def checkexist(id):
        entries = self.db.all()
        for entry in entries:
            if entry['id'] == id:
                self.db.close()
                return True
        self.db.close()
        return False 

    def createEntry(self,id):
        if XPManager.checkexist(id):
            return False
        else:
            entry = {
                "id": id,
                "xp": 0,
                "level": 0,
                "next_level": 1,
                "threshold": 100,
                "booster": None,
                "duration": 0,
                "messages": 0
            }
            self.db.insert(entry)
            print("Entry created.")
            self.db.close()
            return True

      
    @staticmethod
    async def checkrankup(id):
      if self.db == None:
        print("DB is NoneType. returning false.")
        return False
      else:
        entry = self.db.get(where('id') == id)
        next_level = entry['level'] + 1
        threshold = next_level * 100
        
        if entry["xp"] >= threshold: #threshold passed or reached.
          print(f'''User whose current level is {entry["level"]} and who's xp({entry["xp"]} has reache the threshold for the next level, level {next_level}, which is {threshold} will now be ranked up. Returning true. ''')
          entry["level"] = next_level #next level is current level
          entry['next_level'] = next_level + 1
          entry['threshold'] = entry['next_level'] * 100
          entry['xp'] = 0


          self.db.update(entry,Query().id==id)

        #precautions.
        self.db.update(entry,Query().id==id)
        self.db.close()

    def givexp(self,id,range): #range is a list btw.
        user = self.db.get(where('id') == id) #fetch entry matching user's id.
        prev_xp = user['xp'] #get previous xp
        print(f"prev xp: {prev_xp}")

        modifier = user['booster'] #get modifier.

        xp = random.randint(rangee[0],rangee[1]) #Get a random integer between range(inclusive) 1-10 for standard msgs and 1-3 for small message.
        

        if user['xp'] == 0:
              user['xp'] = 1 #set xp to one if its zero.
              print("xp set to 1")
              db.update(user,where('id') == id)
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

            self.db.update(user,Query().id == id)
            self.db.close()

    def getinfo(self,id):
        user = self.db.get(where("id") == id)

        if user == None: 
            errorembed = discord.Embed(title="You haven't send a message yet!",description="How about getting your name registered in the bot's database by sending a message first?",color=discord.Colour.red())
            return errorembed

        returnlist = [user.get("xp", 0), user.get("level", 0), user.get("next_level", 0), user.get("totalxp", 0)]
        db.close()
        return returnlist

    def getdb(self):
        return self.db

    def fixprofile(self,id):
        buggedprofile = self.db.get(where('id') == id)
        fixedprofile = buggedprofile

        if not buggedprofile:
            print("Profile in fixprofile() returned none.")

        elif buggedprofile:
            fixedprofile['next_level'] = buggedprofile['level'] + 1 #set fixed profile's next-level to bugged profile's level + 1
            fixedprofile['threshold'] = fixedprofile['next_level'] * 100 #next_level: 3, threshold = 300  
            self.db.update(fixedprofile, Query().id == id)
            print("profile fixed!")


class XP(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.XPManager = XPManager(bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        if message.author == self.bot.user:
            return

        if message.author.bot:
            return            
        
        
        if isinstance(message.channel, discord.DMChannel):
            return  # Exclude DM messages from XP tracking
        
        await XPManager.checkrankup(message.author.id)

        msg_len = len(message.content.split())
        self.XPManager.createEntry(message.author.id)
        
        if msg_len > 4:
            self.XPManager.givexp(message.author.id, [1, 10]) #for msgs greater than 4 words, give 1-10 xp.
        else:
            print("short msg xp.")
            self.XPManager.givexp(message.author.id, [1, 3]) #for 4 words or less, give 1 to 3 xp.

    @app_commands.command(name="rank",description="See your rank.")
    async def rank(self,interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()

        self.XPManager.fixprofile(interaction.user.id)#just in case the entry is missing some stuff.
        self.XPManager.fixprofile(member)

        if member:
            userinfo = self.XPManager.getinfo(member.id)
            avatar_url = member.display_avatar.url
        else:
            userinfo = self.XPManager.getinfo(interaction.user.id)
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



class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        userList = []
        levels = XPManager(self.bot).getdb()
        
        guild = self.bot.get_guild(interaction.guild_id)  # Get the guild object
        
        for user_data in levels:
            if len(userList) == 5:  # stop if already 5 entries.
                break
            try:
                xp = user_data['xp']
                level = user_data['level']
                userobj = guild.get_member(user_data['id'])  # Get the member from the guild

                if userobj:
                    name = userobj.name
                    userList.append([xp, level, name, userobj])
                else:
                    print(f"User with ID {user_data['id']} not found in the guild.")
            except AttributeError:
                print("1 attribute error")
                pass

        userList = sorted(userList[:5], key=lambda x: (x[1], x[0]), reverse=True) #slice just in case
        await self.generate(userList)

        embed = discord.Embed(title="Leaderboard",description=" ",color=discord.Color.blue())
        file = discord.File(f"temp/lb.png", filename="lb.png")
        embed.set_image(url="attachment://lb.png")
        await interaction.edit_original_response(embed=embed,attachments=[file])



    #code for generating the actual thing
    async def generate(self,userList: list):
        # Open the background image
        background_path = Path("../assets/lb.png")        
        background = Image.open(background_path)

        # Calculate the position to paste the overlay onto the background
        coordinates = {
    '1': (20, 155),
    '2': (20, 266),
    '3': (20, 390),
    '4': (20,500),
    '5': (20,635)
    }

        #Save all images.
        index = 1
        for user in userList:
            await user[3].display_avatar.save(fp=f"temp/pfp{index}.png")
            pfp = Image.open(f'temp/pfp{index}.png')
            pfpResized = pfp.resize((71,67)) #resize
            pfpResized.save(f'temp/pfp{index}.png') #save resized version.
            index += 1

        #open all images:
        for filename in os.listdir('temp'):
            pfp = Image.open(f'temp/{filename}')
            image_path = os.path.join('temp', filename)
            image_name_without_extension = os.path.splitext(filename)[0]
        
            last_letter = image_name_without_extension[-1].lower()  # Get the last letter and convert to lowercase
            
            if last_letter in coordinates:
                target_coordinates = coordinates[last_letter]
                # Paste the pfp onto the lb at the target coordinates
                background.paste(pfp, target_coordinates)
                # Close the images
                pfp.close()


                # Save the result
                output_path = "temp/lb.png"
                background.save(output_path)

        await self.pasteName(userList)

    async def pasteName(self, userList):
        # Open the image
        image_path = "temp/lb.png"
        image = Image.open(image_path)


        # Create a drawing object
        draw = ImageDraw.Draw(image)
        # Choose a font and font size
        font_path = "times.ttf"
        font_size = 32
        font = ImageFont.truetype(font_path, font_size)

        # Choose text color
        text_color = (255, 255, 255)  # White color

        # Calculate text size and position

        coordinates = {
        '1': (180, 160),
        '2': (190, 270),
        '3': (190, 390),
        '4': (190,500),
        '5': (120,637)
        }

    # Paste the text onto the image
        rank = 1
        for user in userList:
            target_coords = coordinates[str(rank)]
            name = user[3].name
            draw.text(target_coords, name, font=font, fill=text_color)
            rank += 1

        # Save or display the modified image
        output_path = "temp/lb.png"
        image.save(output_path)






