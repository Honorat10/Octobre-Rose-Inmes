import json, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

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

def tint(img, color_int):
    r, g, b, _ = to_rgba(color_int)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    a = img.split()[3]
    res = Image.new('RGBA', img.size, (r, g, b, 255))
    res.putalpha(a)
    return res

# 1. Background layer (under the user's photo)
bg = Image.new('RGBA', (W, H), (252, 252, 254, 255))

# Draw subtle background card (shape0 ol15)
if os.path.exists('res/ol15'):
    ol15 = Image.open('res/ol15').convert('RGBA').resize((W, H), Image.Resampling.LANCZOS)
    bg.paste(ol15, (0, 0), ol15)

# Pink backdrop card behind photo (shape1 hY7x)
# In thumb, shape1 is a tilted pink rounded card:
pink_card = Image.new('RGBA', (int(530 * scale), int(530 * scale)), (0, 0, 0, 0))
draw = ImageDraw.Draw(pink_card)
draw.rounded_rectangle((0, 0, pink_card.width, pink_card.height), radius=int(45 * scale), fill=(234, 72, 155, 255))
pink_card_rot = pink_card.rotate(6, expand=True, resample=Image.Resampling.BICUBIC)
bg.paste(pink_card_rot, (int(165 * scale), int(155 * scale)), pink_card_rot)

# 2. Foreground overlay layer (transparent where photo goes)
fg = Image.new('RGBA', (W, H), (0, 0, 0, 0))

# Top Logos
logos = [
    ('logo-inmes-clean.png', 9, 8, 58.0, 58.0),
    ('res/W5x0', 88, 8, 60.0, 60.0),
    ('res/aT9M', 178, 11, 100.5, 56.54),
    ('res/QitP', 298, 11, 54.0, 55.75),
    ('res/CaLk', 395, 16, 90.5, 45.08),
    ('res/WaLs', 503, 7, 67.5, 57.38),
    ('res/rJYC', 588, 18, 37.0, 45.96),
]

for path, x, y, w, h in logos:
    if os.path.exists(path):
        im = Image.open(path).convert('RGBA')
        tw = int(w * scale)
        th = int(h * scale)
        im_resized = im.resize((tw, th), Image.Resampling.LANCZOS)
        fg.paste(im_resized, (int(x * scale), int(y * scale)), im_resized)

# Octobre Rose Card (top right)
# White rounded card with soft shadow
card_w = int(195 * scale)
card_h = int(150 * scale)
card_im = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
cdraw = ImageDraw.Draw(card_im)
cdraw.rounded_rectangle((0, 0, card_w, card_h), radius=int(14 * scale), fill=(255, 255, 255, 255), outline=(240, 240, 245, 255), width=2)

# Ribbon on card
if os.path.exists('res/kf4F'):
    rib = Image.open('res/kf4F').convert('RGBA').resize((int(52 * scale), int(58 * scale)), Image.Resampling.LANCZOS)
    card_im.paste(rib, (int(15 * scale), int(12 * scale)), rib)

# Octobre Rose text
font_title = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', int(23 * scale))
font_sub = ImageFont.truetype('fonts/ABeeZee-Regular.ttf', int(13.5 * scale))

cdraw.text((int(72 * scale), int(10 * scale)), "OCTOBRE", fill=(233, 30, 99, 255), font=font_title)
cdraw.text((int(72 * scale), int(34 * scale)), "ROSE", fill=(233, 30, 99, 255), font=font_title)
cdraw.line([(int(72 * scale), int(64 * scale)), (int(180 * scale), int(64 * scale))], fill=(233, 30, 99, 255), width=int(2 * scale))

cdraw.text((int(15 * scale), int(74 * scale)), "Mois de Sensibilisation\nContre le Cancer du Sein", fill=(30, 30, 35, 255), font=font_sub, align="center")

card_rot = card_im.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
# Add soft shadow for card
card_shadow = Image.new('RGBA', card_rot.size, (0, 0, 0, 0))
sdraw = ImageDraw.Draw(card_shadow)
sdraw.bitmap((0, 0), card_rot.split()[3], fill=(0, 0, 0, 40))
card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(8))
fg.paste(card_shadow, (int(480 * scale) + 4, int(105 * scale) + 6), card_shadow)
fg.paste(card_rot, (int(480 * scale), int(105 * scale)), card_rot)

# Left Date Badge ("23, 24 Octobre 2026")
date_w = int(140 * scale)
date_h = int(108 * scale)
date_card = Image.new('RGBA', (date_w, date_h), (0, 0, 0, 0))
ddraw = ImageDraw.Draw(date_card)
ddraw.rounded_rectangle((0, 0, date_w, date_h), radius=int(14 * scale), fill=(247, 65, 142, 255))
if os.path.exists('res/UwbE'):
    cal_icon = Image.open('res/UwbE').convert('RGBA').resize((int(38 * scale), int(33 * scale)), Image.Resampling.LANCZOS)
    cal_tint = tint(cal_icon, -135949) # white
    date_card.paste(cal_tint, (int(50 * scale), int(10 * scale)), cal_tint)

font_date = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15.5 * scale))
ddraw.text((int(10 * scale), int(54 * scale)), "23, 24 Octobre\n2026", fill=(255, 255, 255, 255), font=font_date, align="center")

date_rot = date_card.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
fg.paste(date_rot, (int(20 * scale), int(190 * scale)), date_rot)

# Contact pill (left)
cont_w = int(185 * scale)
cont_h = int(64 * scale)
cont_card = Image.new('RGBA', (cont_w, cont_h), (0, 0, 0, 0))
pdraw = ImageDraw.Draw(cont_card)
pdraw.rounded_rectangle((0, 0, cont_w, cont_h), radius=int(32 * scale), fill=(255, 255, 255, 240), outline=(245, 230, 238, 255), width=2)
font_phone = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(14 * scale))
pdraw.text((int(15 * scale), int(12 * scale)), "+229 0146097308\n+229 0143096126", fill=(246, 57, 133, 255), font=font_phone)
cont_rot = cont_card.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
fg.paste(cont_rot, (int(10 * scale), int(320 * scale)), cont_rot)

# Bottom white card / fade
if os.path.exists('res/yrCV'):
    yrCV = Image.open('res/yrCV').convert('RGBA').resize((int(698 * scale), int(233 * scale)), Image.Resampling.LANCZOS)
    fg.paste(yrCV, (int(13 * scale), int(463 * scale)), yrCV)

# Bottom background card shape4 (7Lco)
if os.path.exists('res/7Lco'):
    bcard = Image.open('res/7Lco').convert('RGBA').resize((int(1025 * scale), int(416 * scale)), Image.Resampling.LANCZOS)
    bcard_rot = bcard.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
    fg.paste(bcard_rot, (int(-72 * scale), int(583 * scale)), bcard_rot)

# Text: "J'Y SERAI ET TOI?"
font_huge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(38 * scale))
fg_draw = ImageDraw.Draw(fg)

# Calculate positions
fg_draw.text((int(190 * scale), int(565 * scale)), "J'Y SERAI ET", fill=(55, 55, 60, 255), font=font_huge)
fg_draw.text((int(280 * scale), int(608 * scale)), "TOI?", fill=(246, 57, 133, 255), font=font_huge)

# Bottom right: Marché Ganhi button
btn_w = int(205 * scale)
btn_h = int(61 * scale)
btn_im = Image.new('RGBA', (btn_w, btn_h), (0, 0, 0, 0))
bdraw = ImageDraw.Draw(btn_im)
bdraw.rounded_rectangle((0, 0, btn_w, btn_h), radius=int(12 * scale), fill=(247, 65, 142, 255))
if os.path.exists('res/DuP1'):
    pin = Image.open('res/DuP1').convert('RGBA').resize((int(46 * scale), int(55 * scale)), Image.Resampling.LANCZOS)
    pin_tint = tint(pin, -1)
    btn_im.paste(pin_tint, (int(8 * scale), int(3 * scale)), pin_tint)

font_btn = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', int(21 * scale))
bdraw.text((int(58 * scale), int(6 * scale)), "MARCHÉ", fill=(255, 255, 255, 255), font=font_btn)
bdraw.text((int(58 * scale), int(30 * scale)), "GANHI", fill=(255, 255, 255, 255), font=font_btn)
fg.paste(btn_im, (int(484 * scale), int(573 * scale)), btn_im)

# "PARCE QUE NOUS CHOISISSONS LA PREVENTION"
font_prev = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15 * scale))
fg_draw.text((int(484 * scale), int(642 * scale)), "PARCE QUE NOUS\nCHOISISSONS LA", fill=(30, 30, 35, 255), font=font_prev)
font_prev_pink = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15 * scale))
fg_draw.text((int(484 * scale), int(676 * scale)), "PREVENTION", fill=(247, 65, 142, 255), font=font_prev_pink)

# Megaphone (correctly oriented: mirrored + rotated so cone faces top-left towards PREVENTION)
if os.path.exists('res/Pmuw'):
    mega = Image.open('res/Pmuw').convert('RGBA')
    mega_mirror = ImageOps.mirror(mega)
    mega_rot = mega_mirror.rotate(-30, expand=True, resample=Image.Resampling.BICUBIC)
    mw = int(72 * scale)
    mh = int(72 * scale)
    mega_final = mega_rot.resize((mw, mh), Image.Resampling.LANCZOS)
    fg.paste(mega_final, (int(630 * scale), int(638 * scale)), mega_final)

# Large 3D Pink Ribbon on bottom left (OVER the lower card and photo!)
if os.path.exists('res/rn2m'):
    rib_lg = Image.open('res/rn2m').convert('RGBA').resize((int(515 * scale), int(410 * scale)), Image.Resampling.LANCZOS)
    rib_rot = rib_lg.rotate(-8, expand=True, resample=Image.Resampling.BICUBIC)
    fg.paste(rib_rot, (int(-34 * scale), int(407 * scale)), rib_rot)

bg.save('template_bg.png')
fg.save('template_overlay.png')

# Also save a composite with GPcC to verify against thumb!
comp = bg.copy()
if os.path.exists('res/GPcC'):
    photo = Image.open('res/GPcC').convert('RGBA')
    # Photo card size and position (shape2 Tnzw)
    pw = int(527 * scale)
    ph = int(527 * scale)
    # Mask rounded rectangle
    pmask = Image.new('L', (pw, ph), 0)
    pdraw = ImageDraw.Draw(pmask)
    pdraw.rounded_rectangle((0, 0, pw, ph), radius=int(45 * scale), fill=255)
    
    photo_fit = photo.resize((pw, int(pw * photo.height / photo.width)), Image.Resampling.LANCZOS)
    # Crop to square
    top = int((photo_fit.height - ph) * 0.2)
    photo_cropped = photo_fit.crop((0, top, pw, top + ph))
    photo_cropped.putalpha(pmask)
    photo_rot = photo_cropped.rotate(6, expand=True, resample=Image.Resampling.BICUBIC)
    
    comp.paste(photo_rot, (int(100 * scale), int(105 * scale)), photo_rot)

comp.paste(fg, (0, 0), fg)
comp.save('test_verification_composite.png')

print("All master assets generated successfully!")
