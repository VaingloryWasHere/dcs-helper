from PIL import Image, ImageDraw, ImageFont
import random
import os
import asyncio 
import discord
from discord.ext import commands
from discord import app_commands

class Verifier(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.processing = False

    async def generate(self):
        try:
            self.processing = True
            original_image = Image.open("../assets/strat.png")
            buffer_image = original_image.copy()
            random_text = ''.join(random.choice(['dcsverify','darkstories','vanitysystemsinc','skynetIsHere']))
            draw = ImageDraw.Draw(buffer_image)

            # Define font size and font path
            font_size = 30
            font_path = "../assets/times.ttf"  # Replace with the actual path to a font file

            # Load the font
            font = ImageFont.truetype(font_path, font_size)

            # Get the size of the text
            text_width, text_height = draw.textsize(random_text, font=font)

            # Calculate the position to center the text on the image
            image_width, image_height = buffer_image.size
            x_position = (image_width - text_width) // 2
            y_position = (image_height - text_height) // 2

            # Set text color
            text_color = (255, 255, 255)  # White color

            # Draw the text on the image
            draw.text((x_position, y_position), random_text, font=font, fill=text_color)

            # Save the modified image as 'buffer.png'
            buffer_image.save("buffer.png")

            # Close the images
            original_image.close()
            buffer_image.close()

            return True, random_text

        except Exception as error:
            return False, error

    @app_commands.command(name="verify",description="Verify yourself.")
    async def verify(self, interaction: discord.Interaction):
        if self.processing == True:
            await interaction.response.send_message("Another verification is being processed! If that was you, consider waiting sometime before trying again.")
            return

        await interaction.response.defer()
        await interaction.edit_original_response(content="Processing..")

        res, code = await self.generate()
        if res == False:
            inform = await interaction.edit_original_response(content=f"Error encountered: ```{code}```")
            await asyncio.sleep(10)
            await inform.delete()
            return

        img = discord.File(fp='buffer.png')
        await interaction.user.send(file=img)
        await interaction.user.send("Enter the text you see within 30 seconds.")

        try:
            attempt = await self.bot.wait_for('message',check=lambda x: x.author == interaction.user and isinstance(x.channel,discord.DMChannel),timeout=30)
            print(attempt.content)
            print(code)
            if attempt.content == code:
                await interaction.user.send("verified!")
                os.remove("buffer.png")
                self.processing = False

            elif attempt.content != code:
                await interaction.user.send("Wrong code!")
                os.remove("buffer.png")
                self.processing = False

        except asyncio.TimeoutError:
            self.processing = False
            await interaction.user.send("timeout!")
            os.remove("buffer.png")

Verifier(commands.Bot(command_prefix=".",intents=discord.Intents.all()))

