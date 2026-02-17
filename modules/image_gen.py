from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_welcome_card(user_name):
    # Load background
    bg = Image.open("assets/background.jpg").convert("RGBA")
    draw = ImageDraw.Draw(bg)
    
    # Load fonts (Ensure you have a .ttf file in your path)
    font_path = "assets/font.ttf" 
    font = ImageFont.truetype(font_path, 60) if os.path.exists(font_path) else ImageFont.load_default()

    text = f"WELCOME, {user_name}!"
    
    # Calculate text position (Center)
    w, h = bg.size
    tw, th = draw.textsize(text, font=font)
    position = ((w - tw) // 2, (h - th) // 2)

    # Draw Shadow
    draw.text((position[0]+3, position[1]+3), text, font=font, fill=(0, 0, 0, 150))
    # Draw Main Text
    draw.text(position, text, font=font, fill=(255, 255, 255))

    output_path = f"temp_welcome_{user_name}.png"
    bg.save(output_path)
    return output_path
