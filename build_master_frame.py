import json, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

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

# -------------------------------------------------------------
# 1. Background layer: template_bg.png
# -------------------------------------------------------------
bg = Image.new('RGBA', (W, H), (252, 252, 254, 255))

# Subtle background shape (shape0 ol15)
if os.path.exists('res/ol15'):
    ol15 = Image.open('res/ol15').convert('RGBA')
    ol15_res = ol15.resize((int(970 * scale), int(948 * scale)), Image.Resampling.LANCZOS)
    bg.paste(ol15_res, (int(-109 * scale), int(-125 * scale)), ol15_res)

# Pink backdrop card (shape1): x=152, y=141, w=527.08, h=527.08, rot=-6, opacity=52%
pcard_w = int(527.08 * scale)
pcard_h = int(527.08 * scale)
pink_card = Image.new('RGBA', (pcard_w, pcard_h), (0, 0, 0, 0))
pdraw = ImageDraw.Draw(pink_card)
# Fill color -1423205 is #ea489b, 52% opacity -> alpha = 133
pdraw.rounded_rectangle((0, 0, pcard_w, pcard_h), radius=105, fill=(234, 72, 155, 133))
pink_card_rot = pink_card.rotate(6, expand=True, resample=Image.Resampling.BICUBIC)

cx1 = (152 + 527.08 / 2.0) * scale
cy1 = (141 + 527.08 / 2.0) * scale
bg.paste(pink_card_rot, (int(cx1 - pink_card_rot.width / 2.0), int(cy1 - pink_card_rot.height / 2.0)), pink_card_rot)

# Save template_bg.png
bg.save('template_bg.png')
bg.save('assets/template_bg.png')

# -------------------------------------------------------------
# 2. Foreground overlay: template_overlay.png
# -------------------------------------------------------------
fg = Image.new('RGBA', (W, H), (0, 0, 0, 0))

# Top right white card (shape3): x=487, y=112, w=189.72, h=148.93, rot=-7
cw = int(189.72 * scale)
ch = int(148.93 * scale)
card_im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
cdraw = ImageDraw.Draw(card_im)
cdraw.rounded_rectangle((0, 0, cw, ch), radius=int(14 * scale), fill=(255, 255, 255, 255), outline=(235, 235, 240, 255), width=2)

# Ribbon on card (shape9: x=492, y=124, w=52, h=58) -> relative to 487, 112 is (5, 12)
if os.path.exists('res/kf4F'):
    rib = Image.open('res/kf4F').convert('RGBA').resize((int(52 * scale), int(58 * scale)), Image.Resampling.LANCZOS)
    card_im.paste(rib, (int((492 - 487) * scale), int((124 - 112) * scale)), rib)

font_title = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', int(22.5 * scale))
font_sub = ImageFont.truetype('fonts/ABeeZee-Regular.ttf', int(13 * scale))

cdraw.text((int((536 - 487) * scale), int((120 - 112) * scale)), "OCTOBRE", fill=(233, 30, 99, 255), font=font_title)
cdraw.text((int((537 - 487) * scale), int((144 - 112) * scale)), "ROSE", fill=(233, 30, 99, 255), font=font_title)
cdraw.line([(int((542 - 487) * scale), int((175 - 112) * scale)), (int((542 + 122 - 487) * scale), int((175 - 112) * scale))], fill=(233, 30, 99, 255), width=int(2.5 * scale))
cdraw.text((int((500 - 487) * scale), int((184 - 112) * scale)), "Mois de Sensibilisation\nContre le Cancer du Sein", fill=(30, 30, 35, 255), font=font_sub, align="center")

cx3 = (487 + 189.72 / 2.0) * scale
cy3 = (112 + 148.93 / 2.0) * scale
card_rot = card_im.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)

# Soft shadow for card
c_sh = Image.new('RGBA', card_rot.size, (0, 0, 0, 0))
ImageDraw.Draw(c_sh).bitmap((0, 0), card_rot.split()[3], fill=(0, 0, 0, 35))
c_sh = c_sh.filter(ImageFilter.GaussianBlur(8))
fg.paste(c_sh, (int(cx3 - card_rot.width / 2.0) + 4, int(cy3 - card_rot.height / 2.0) + 6), c_sh)
fg.paste(card_rot, (int(cx3 - card_rot.width / 2.0), int(cy3 - card_rot.height / 2.0)), card_rot)

# Bottom background card shape4 (7Lco: x=-72, y=583, w=1024.98, h=416.69, rot=-7)
if os.path.exists('res/7Lco'):
    bcard = Image.open('res/7Lco').convert('RGBA').resize((int(1024.98 * scale), int(416.69 * scale)), Image.Resampling.LANCZOS)
    cx4 = (-72 + 1024.98 / 2.0) * scale
    cy4 = (583 + 416.69 / 2.0) * scale
    bcard_rot = bcard.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
    fg.paste(bcard_rot, (int(cx4 - bcard_rot.width / 2.0), int(cy4 - bcard_rot.height / 2.0)), bcard_rot)

# Bottom white gradient fade shape5 (yrCV: x=13, y=463, w=698, h=233.5, rot=0)
if os.path.exists('res/yrCV'):
    yrCV = Image.open('res/yrCV').convert('RGBA').resize((int(698 * scale), int(233.5 * scale)), Image.Resampling.LANCZOS)
    fg.paste(yrCV, (int(13 * scale), int(463 * scale)), yrCV)

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
for path, lx, ly, lw, lh in logos:
    if os.path.exists(path):
        lim = Image.open(path).convert('RGBA').resize((int(lw * scale), int(lh * scale)), Image.Resampling.LANCZOS)
        fg.paste(lim, (int(lx * scale), int(ly * scale)), lim)

# Date Badge (shape29: x=22, y=194, w=137.92, h=108.27, rot=-7)
db_w = int(137.92 * scale)
db_h = int(108.27 * scale)
db_im = Image.new('RGBA', (db_w, db_h), (0, 0, 0, 0))
db_draw = ImageDraw.Draw(db_im)
db_draw.rounded_rectangle((0, 0, db_w, db_h), radius=int(22 * scale), fill=(247, 65, 142, 255))
if os.path.exists('res/UwbE'):
    cal_im = tint(Image.open('res/UwbE').convert('RGBA').resize((int(41 * scale), int(35.28 * scale)), Image.Resampling.LANCZOS), -135949)
    db_im.paste(cal_im, (int((59 - 22) * scale), int((199 - 194) * scale)), cal_im)
font_date = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15.5 * scale))
db_draw.text((int(14 * scale), int(48 * scale)), "23, 24 Octobre\n2026", fill=(255, 255, 255, 255), font=font_date, align="center")

cx_db = (22 + 137.92 / 2.0) * scale
cy_db = (194 + 108.27 / 2.0) * scale
db_rot = db_im.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
fg.paste(db_rot, (int(cx_db - db_rot.width / 2.0), int(cy_db - db_rot.height / 2.0)), db_rot)

# Contact pill (shape32: x=5, y=325, w=188.55, h=66.22, rot=-7)
cp_w = int(188.55 * scale)
cp_h = int(66.22 * scale)
cp_im = Image.new('RGBA', (cp_w, cp_h), (0, 0, 0, 0))
cp_draw = ImageDraw.Draw(cp_im)
cp_draw.rounded_rectangle((0, 0, cp_w, cp_h), radius=int(33 * scale), fill=(255, 255, 255, 245), outline=(245, 225, 235, 255), width=2)
font_phone = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(14.5 * scale))
cp_draw.text((int((33 - 5) * scale), int((343 - 325) * scale)), "+229 0146097308\n+229 0143096126", fill=(246, 57, 133, 255), font=font_phone)

cx_cp = (5 + 188.55 / 2.0) * scale
cy_cp = (325 + 66.22 / 2.0) * scale
cp_rot = cp_im.rotate(7, expand=True, resample=Image.Resampling.BICUBIC)
fg.paste(cp_rot, (int(cx_cp - cp_rot.width / 2.0), int(cy_cp - cp_rot.height / 2.0)), cp_rot)

# Text "J'Y SERAI ET TOI?" (text21: 177, 570)
font_serai = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(35.02 * scale))
fg_draw = ImageDraw.Draw(fg)

line1 = "J'Y SERAI ET"
line2 = "TOI?"
bbox1 = fg_draw.textbbox((0, 0), line1, font=font_serai)
w1 = bbox1[2] - bbox1[0]
bbox2 = fg_draw.textbbox((0, 0), line2, font=font_serai)
w2 = bbox2[2] - bbox2[0]

cx_txt = int((177 + 269 / 2.0) * scale)
y_txt = int(570 * scale)
fg_draw.text((cx_txt - w1 // 2, y_txt), line1, fill=(68, 68, 68, 255), font=font_serai)
fg_draw.text((cx_txt - w2 // 2, y_txt + int(42 * scale)), line2, fill=(246, 57, 133, 255), font=font_serai)

# Marché Ganhi button (shape7: 484, 573, w=205, h=61, rot=0)
btn_w = int(205 * scale)
btn_h = int(61 * scale)
btn_im = Image.new('RGBA', (btn_w, btn_h), (0, 0, 0, 0))
bdraw = ImageDraw.Draw(btn_im)
bdraw.rounded_rectangle((0, 0, btn_w, btn_h), radius=int(14 * scale), fill=(247, 65, 142, 255))
if os.path.exists('res/DuP1'):
    pin = tint(Image.open('res/DuP1').convert('RGBA').resize((int(46 * scale), int(55.3 * scale)), Image.Resampling.LANCZOS), -1)
    btn_im.paste(pin, (int((492 - 484) * scale), int((574 - 573) * scale)), pin)

font_btn = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', int(21 * scale))
bdraw.text((int((545 - 484) * scale), int((574 - 573) * scale)), "MARCHÉ", fill=(255, 255, 255, 255), font=font_btn)
bdraw.text((int((541 - 484) * scale), int((599 - 573) * scale)), "GANHI", fill=(255, 255, 255, 255), font=font_btn)
fg.paste(btn_im, (int(484 * scale), int(573 * scale)), btn_im)

# "PARCE QUE NOUS CHOISISSONS LA PREVENTION" (text24: 480, 634)
font_prev = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', int(15 * scale))
fg_draw.text((int(484 * scale), int(642 * scale)), "PARCE QUE NOUS\nCHOISISSONS LA", fill=(30, 30, 35, 255), font=font_prev)
fg_draw.text((int(484 * scale), int(676 * scale)), "PREVENTION", fill=(247, 65, 142, 255), font=font_prev)

# Megaphone (shape25: 640, 651, w=65.8, h=65.6, rot=30, flipped horizontally)
if os.path.exists('res/Pmuw'):
    mega = Image.open('res/Pmuw').convert('RGBA')
    mega_mirror = ImageOps.mirror(mega)
    mega_rot = mega_mirror.rotate(-30, expand=True, resample=Image.Resampling.BICUBIC)
    mw = int(68 * scale)
    mh = int(68 * scale)
    mega_final = mega_rot.resize((mw, mh), Image.Resampling.LANCZOS)
    cx_mg = (640 + 65.84 / 2.0) * scale
    cy_mg = (651 + 65.59 / 2.0) * scale
    fg.paste(mega_final, (int(cx_mg - mega_final.width / 2.0), int(cy_mg - mega_final.height / 2.0)), mega_final)

# Large 3D Pink Ribbon (shape14: -34, 407, w=514.5, h=409.26, rot=8)
if os.path.exists('res/rn2m'):
    rib_lg = Image.open('res/rn2m').convert('RGBA').resize((int(514.5 * scale), int(409.26 * scale)), Image.Resampling.LANCZOS)
    cx_rib = (-34 + 514.5 / 2.0) * scale
    cy_rib = (407 + 409.26 / 2.0) * scale
    rib_rot = rib_lg.rotate(-8, expand=True, resample=Image.Resampling.BICUBIC)
    fg.paste(rib_rot, (int(cx_rib - rib_rot.width / 2.0), int(cy_rib - rib_rot.height / 2.0)), rib_rot)

# Save template_overlay.png
fg.save('template_overlay.png')
fg.save('assets/template_overlay.png')

print("Master template_bg.png and template_overlay.png generated successfully!")
