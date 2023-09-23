from PIL import Image
from PIL import Image, ImageDraw, ImageFont

# Open the image
image_path = "lb.png"
image = Image.open(image_path)

# Define the text to be pasted
text = "Hello, World!"

# Create a drawing object
draw = ImageDraw.Draw(image)

# Choose a font and font size
font_path = "times.ttf"
font_size = 32
font = ImageFont.truetype(font_path, font_size)

# Choose text color
text_color = (255, 255, 255)  # White color

# Calculate text size and position

pos = (180, 160)
pos2 = (190, 270)
pos3 = (190, 390)
pos4 = (190,500)
pos5 = (190,637)


# Paste the text onto the image
draw.text(pos, text, font=font, fill=text_color)
draw.text(pos2, text, font=font, fill=text_color)
draw.text(pos3, text, font=font, fill=text_color)
draw.text(pos4, text, font=font, fill=text_color)
draw.text(pos5, text, font=font, fill=text_color)

# Save or display the modified image
output_path = "path_to_output_image.png"
image.save(output_path)

coordinates = {
    '1': (180, 160),
    '2': (190, 270),
    '3': (190, 390),
    '4': (190,500),
    '5': (120,637)
    }

