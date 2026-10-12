import json, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor

# Load data
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
    # Tint only non-transparent pixels
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    alpha = img.split()[3]
    color_img = Image.new('RGBA', img.size, (r, g, b, 255))
    color_img.putalpha(alpha)
    return color_img

print("Setup ready")
