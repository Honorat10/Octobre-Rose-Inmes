import json, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

with open('data.plab') as f:
    data = json.load(f)

bundle = data['objectsBundle']
order = data['objectsIds']

W, H = 1600, 1600
scale = W / 704.0

def to_rgba(val, alpha=255):
    val = val & 0xffffffff
    r = (val >> 16) & 0xff
    g = (val >> 8) & 0xff
    b = val & 0xff
    return (r, g, b, alpha)

def apply_color_overlay(img, color_int):
    r, g, b, _ = to_rgba(color_int)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    alpha = img.split()[3]
    color_img = Image.new('RGBA', img.size, (r, g, b, 255))
    color_img.putalpha(alpha)
    return color_img

def apply_shadow(img, shadow_color, radius=8, offset=(0, 0)):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, _ = to_rgba(shadow_color)
    alpha = img.split()[3]
    # expand canvas for blur
    pad = int(radius * 3)
    shadow = Image.new('RGBA', (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    shadow_fill = Image.new('RGBA', img.size, (r, g, b, 180))
    shadow_fill.putalpha(alpha)
    shadow.paste(shadow_fill, (pad + offset[0], pad + offset[1]), shadow_fill)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius))
    
    # paste img on top
    shadow.paste(img, (pad, pad), img)
    return shadow, pad

# Let's create two layers:
# 1. Background image (everything before shape2, plus pink card behind photo)
# 2. Foreground overlay (everything on top of the photo)
bg_canvas = Image.new('RGBA', (W, H), (250, 250, 252, 255))
fg_canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))

# Try loading available fonts
font_black = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(34 * scale))
font_sub = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15 * scale))
font_pink_italic = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', int(22 * scale))
font_date = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(16 * scale))
font_contacts = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(14 * scale))
font_abeezee = ImageFont.truetype('fonts/ABeeZee-Regular.ttf', int(13 * scale))

print("Script template ready")
