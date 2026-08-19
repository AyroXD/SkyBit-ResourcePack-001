from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import zipfile, shutil, json, random, hashlib, math, os

ready=Path('build/SkyBit-ResourcePack')
ready.mkdir(parents=True,exist_ok=True)
texroot=ready/'assets/skybit/textures/item'

PAL={
 'basic':('#082c35','#13808b','#52e5d4','#d9fff8','#6b4328','#8fa7ad','#a4fff4','#21505a'),
 'rare':('#0c1d4e','#214b9c','#58a9ff','#d9ecff','#4d382b','#9db2d0','#9bd4ff','#2f5bb1'),
 'epic':('#25103f','#5a2685','#b968ff','#f0d4ff','#4b315a','#a593be','#e4aaff','#743aa1'),
 'legendary':('#4a2103','#99510b','#ffc247','#fff0a6','#6a3d16','#c89c4f','#fff29d','#d17a13'),
 'mythic':('#0b0718','#321052','#8b3eff','#63f1ff','#24132f','#7d64a5','#a8ffff','#5b1ba4'),
 'vote':('#0d351d','#1c7540','#62dd78','#d8ffe0','#4c3d27','#8fb89a','#a9ffb9','#2b8e4f'),
 'storm':('#071d2b','#0f5366','#35d6e8','#b6fbff','#3a5060','#86aab3','#8df7ff','#177f91'),
 'ember':('#2a0b08','#711c12','#e95b23','#ffd27b','#4b2d22','#b46c42','#ff9f54','#9d2e15'),
 'void':('#100819','#331341','#8c3fa7','#e9b6ff','#2a2534','#746984','#d79cff','#5b236d'),
 'neutral':('#111820','#2c3945','#6d7d89','#e8f1f5','#4a3425','#a0adb3','#d9ffff','#465b66'),
 'gold':('#4b2f03','#a06a0c','#f7c743','#fff2a3','#55371a','#bb9855','#fff5b9','#c78413'),
}

def hexrgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def shade(c,delta): return tuple(max(0,min(255,x+delta)) for x in c)

def tile_texture(theme, special=None):
    colors=[hexrgb(x) for x in PAL[theme]]
    im=Image.new('RGBA',(64,64),(0,0,0,0)); d=ImageDraw.Draw(im)
    rng=random.Random(theme+(special or ''))
    tilecols=[colors[0],colors[1],colors[2],colors[3],colors[4],colors[5],colors[6],colors[7],
              shade(colors[1],-12),shade(colors[1],14),shade(colors[2],-18),shade(colors[2],18),
              shade(colors[4],-10),shade(colors[5],15),shade(colors[6],-20),colors[3]]
    for idx,c in enumerate(tilecols):
        x=(idx%4)*16; y=(idx//4)*16
        d.rectangle((x,y,x+15,y+15), fill=c+(255,))
        d.line((x,y,x+15,y), fill=shade(c,20)+(255,))
        d.line((x,y,x,y+15), fill=shade(c,10)+(255,))
        d.line((x,y+15,x+15,y+15), fill=shade(c,-25)+(255,))
        d.line((x+15,y,x+15,y+15), fill=shade(c,-18)+(255,))
        for _ in range(5):
            px=x+rng.randint(2,13); py=y+rng.randint(2,13)
            d.point((px,py), fill=shade(c,rng.choice([-12,-8,10,14]))+(255,))
    if special in ('legendary','mythic'):
        glow=colors[6]
        for idx in [3,6,11,15]:
            x=(idx%4)*16; y=(idx//4)*16
            d.rectangle((x+5,y+2,x+10,y+13), outline=glow+(255,))
            d.line((x+3,y+8,x+12,y+8), fill=colors[3]+(255,), width=1)
            d.point((x+8,y+8), fill=(255,255,255,255))
    return im

def save_atlas(rel,theme,special=None):
    p=texroot/rel; p.parent.mkdir(parents=True,exist_ok=True); tile_texture(theme,special).save(p)

for tier in ['basic','rare','epic','legendary','mythic','vote']:
    if (texroot/f'crates/{tier}.png').exists(): save_atlas(f'crates/{tier}.png',tier,special=tier)
    if (texroot/f'keys/{tier}.png').exists(): save_atlas(f'keys/{tier}.png',tier,special=tier)
    if (texroot/f'fragments/{tier}.png').exists(): save_atlas(f'fragments/{tier}.png',tier,special=tier)
for tier in ['basic','rare','epic','legendary','vote']:
    if (texroot/f'mines/{tier}_crystal.png').exists(): save_atlas(f'mines/{tier}_crystal.png',tier,special=tier)
for rel,theme in [
 ('gear/weapons/skyfang_blade.png','storm'),('gear/weapons/stormcaller_spear.png','storm'),('gear/weapons/frostbite_bow.png','rare'),
 ('gear/weapons/ember_cleaver.png','ember'),('gear/weapons/void_reaver.png','void'),('gear/tools/titan_pickaxe.png','gold'),
 ('contracts/daily_contract.png','basic'),('contracts/weekly_contract.png','epic'),('afk/premium_pass.png','basic'),
 ('currency/skycoin.png','gold'),('guilds/guild_seal.png','basic'),('bounty/bounty_token.png','ember'),('collections/token.png','basic')]:
    if (texroot/rel).exists(): save_atlas(rel,theme)
for rel in ['renown/bronze.png','renown/gold.png','renown/master.png','renown/platinum.png','renown/silver.png']:
    if (texroot/rel).exists(): save_atlas(rel,'gold' if 'gold' in rel or 'bronze' in rel else 'epic' if 'master' in rel else 'rare')
for rel,theme in [('vip/vip_badge.png','basic'),('vip/knight_badge.png','rare'),('vip/baron_badge.png','epic'),('vip/king_badge.png','legendary'),('vip/emperor_badge.png','mythic')]:
    if (texroot/rel).exists(): save_atlas(rel,theme,special='mythic' if theme=='mythic' else None)
for setname,theme in [('stormguard','storm'),('emberforged','ember'),('voidwarden','void')]:
    for piece in ['helmet','chestplate','leggings','boots']:
        rel=f'gear/armor/{setname}_{piece}.png'
        if (texroot/rel).exists(): save_atlas(rel,theme,special='mythic' if setname=='voidwarden' else None)

save_atlas('afk/beacon.png','mythic','mythic')

def icon_canvas(bg=(9,18,25,255)):
    im=Image.new('RGBA',(64,64),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((4,4,59,59),radius=10,fill=bg,outline=(50,80,92,255),width=2)
    d.rectangle((8,8,55,10),fill=(255,255,255,18))
    return im,d

def draw_gem(rel,theme,shape='diamond'):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]]
    d.ellipse((13,50,51,56),fill=(0,0,0,90))
    pts=[(32,8),(50,25),(43,47),(32,56),(16,45),(14,24)]
    d.polygon(pts,fill=c[0],outline=c[6]); d.polygon([(32,12),(45,26),(39,43),(32,50),(20,42),(19,26)],fill=c[1]); d.polygon([(32,13),(32,49),(22,40),(22,27)],fill=c[2]); d.polygon([(33,15),(42,27),(37,33),(33,36)],fill=c[3]); d.rectangle((48,11,52,15),fill=c[6])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_medal(rel,theme):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]]
    d.polygon([(20,9),(28,9),(33,29),(25,31)],fill=c[1]);d.polygon([(36,9),(44,9),(39,31),(31,29)],fill=c[2]);d.ellipse((15,23,49,57),fill=c[0],outline=c[6],width=2);d.ellipse((20,28,44,52),fill=c[1]);d.polygon([(32,30),(35,38),(44,38),(37,43),(40,51),(32,46),(24,51),(27,43),(20,38),(29,38)],fill=c[3])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_compass(rel,theme='legendary'):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]]
    d.ellipse((10,10,54,54),fill=c[0],outline=c[5],width=3);d.ellipse((15,15,49,49),fill=(12,25,34),outline=c[2],width=2);d.polygon([(32,16),(37,31),(32,28),(27,31)],fill=c[3]);d.polygon([(32,48),(27,33),(32,36),(37,33)],fill=(244,74,84));d.ellipse((29,29,35,35),fill=c[6])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_dust(rel):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL['epic']]
    for x,y,r in [(22,35,8),(34,23,10),(45,39,8),(31,47,6)]:
        d.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=c[0],outline=c[6]); d.polygon([(x,y-r+3),(x+r-3,y),(x,y+r-3),(x-r+3,y)],fill=c[2]); d.line((x,y-r+3,x,y),fill=c[3],width=2)
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_core(rel,theme='epic'):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]]
    d.polygon([(32,7),(48,20),(44,49),(32,57),(19,48),(15,20)],fill=c[0],outline=c[6]);d.polygon([(32,12),(43,23),(39,44),(32,51),(24,43),(21,23)],fill=c[1]);d.rectangle((29,18,35,43),fill=c[2]);d.rectangle((23,28,41,34),fill=c[2]);d.rectangle((30,20,34,32),fill=c[3])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_food(rel):
    im,d=icon_canvas((23,19,16,255));d.ellipse((10,29,54,54),fill=(86,44,28),outline=(232,156,73),width=2);d.ellipse((14,26,50,47),fill=(222,139,65));d.ellipse((17,28,47,43),fill=(245,185,102));d.ellipse((21,30,28,36),fill=(74,171,83));d.ellipse((34,31,42,38),fill=(173,53,45));d.rectangle((11,48,53,52),fill=(75,41,31))
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_prof(rel,theme,symbol):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]];d.ellipse((12,12,52,52),fill=c[0],outline=c[6],width=2);d.ellipse((17,17,47,47),fill=c[1])
    if symbol=='pick': d.line((24,42,40,20),fill=c[3],width=5);d.line((20,23,44,18),fill=c[2],width=5)
    elif symbol=='fish': d.ellipse((20,25,41,39),fill=c[2]);d.polygon([(41,32),(51,23),(49,41)],fill=c[3]);d.point((25,30),fill=(5,10,15))
    elif symbol=='leaf': d.ellipse((20,19,42,43),fill=c[2]);d.line((31,42,36,20),fill=c[3],width=3);d.line((31,31,23,25),fill=c[3],width=2)
    elif symbol=='axe': d.line((26,44,37,20),fill=c[4],width=5);d.polygon([(33,17),(46,20),(39,31),(30,27)],fill=c[2])
    else: d.polygon([(32,17),(42,26),(38,43),(26,43),(22,26)],fill=c[2]);d.rectangle((29,28,35,38),fill=c[3])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

def draw_ui(rel,theme,symbol):
    im,d=icon_canvas(); c=[hexrgb(x) for x in PAL[theme]];d.rounded_rectangle((14,14,50,50),radius=8,fill=c[0],outline=c[6],width=2)
    if symbol=='profile': d.ellipse((25,19,39,33),fill=c[2]);d.ellipse((19,33,45,48),fill=c[1])
    elif symbol=='menu':
        for y in (21,31,41): d.rectangle((20,y,44,y+4),fill=c[2])
    elif symbol=='settings': d.ellipse((22,22,42,42),outline=c[2],width=5);d.ellipse((28,28,36,36),fill=c[6])
    elif symbol=='leaderboard': d.rectangle((20,32,26,44),fill=c[1]);d.rectangle((29,24,35,44),fill=c[2]);d.rectangle((38,29,44,44),fill=c[3])
    elif symbol=='quest': d.rectangle((20,18,44,46),fill=(224,205,158));d.rectangle((24,24,40,27),fill=c[1]);d.rectangle((24,32,37,35),fill=c[2])
    elif symbol=='booster': d.polygon([(32,17),(39,29),(47,32),(39,35),(32,47),(25,35),(17,32),(25,29)],fill=c[2]);d.ellipse((28,28,36,36),fill=c[3])
    elif symbol=='links': d.arc((17,23,34,40),90,270,fill=c[2],width=4);d.arc((30,23,47,40),270,90,fill=c[3],width=4);d.line((27,31,37,31),fill=c[6],width=4)
    else: d.polygon([(20,18),(44,18),(47,42),(32,49),(17,42)],fill=c[1],outline=c[6]);d.polygon([(32,22),(36,31),(44,31),(38,36),(40,44),(32,39),(24,44),(26,36),(20,31),(28,31)],fill=c[3])
    p=texroot/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)

if (texroot/'enchant/arcane_dust.png').exists(): draw_dust('enchant/arcane_dust.png')
if (texroot/'enchant/enchant_core.png').exists(): draw_core('enchant/enchant_core.png','epic')
if (texroot/'events/supply_beacon.png').exists(): draw_core('events/supply_beacon.png','rare')
if (texroot/'achievements/medal.png').exists(): draw_medal('achievements/medal.png','legendary')
if (texroot/'treasure/treasure_compass.png').exists(): draw_compass('treasure/treasure_compass.png')
if (texroot/'cozy/hearty_stew.png').exists(): draw_food('cozy/hearty_stew.png')
for rel,theme in [('relics/relic_shard.png','epic'),('relics/prosperity.png','legendary'),('relics/wisdom.png','rare'),('relics/fortune.png','vote'),('relics/titan.png','ember'),('relics/voyager.png','basic')]:
    if (texroot/rel).exists(): draw_gem(rel,theme)
for rel,theme,sym in [('professions/miner.png','basic','pick'),('professions/fisher.png','rare','fish'),('professions/farmer.png','vote','leaf'),('professions/woodcutter.png','legendary','axe'),('professions/hunter.png','ember','shield')]:
    if (texroot/rel).exists(): draw_prof(rel,theme,sym)
for rel,theme,sym in [('ui/profile.png','basic','profile'),('ui/menu.png','basic','menu'),('ui/settings.png','neutral','settings'),('ui/leaderboard.png','legendary','leaderboard'),('ui/questhub.png','epic','quest'),('ui/booster.png','rare','booster'),('ui/links.png','basic','links'),('ui/serverpass.png','legendary','pass')]:
    if (texroot/rel).exists(): draw_ui(rel,theme,sym)

P=256
im=Image.new('RGBA',(P,P),(5,12,19,255));d=ImageDraw.Draw(im)
for y in range(0,P,16): d.line((0,y,P,y),fill=(12,29,40,255))
for x in range(0,P,16): d.line((x,0,x,P),fill=(10,24,34,255))
for r,col in [(108,(8,39,50,255)),(94,(10,66,77,255)),(79,(13,47,59,255))]: d.ellipse((128-r,128-r,128+r,128+r),fill=col)
shield=[(128,35),(191,71),(183,159),(128,211),(73,159),(65,71)]
d.polygon(shield,fill=(7,27,38),outline=(73,231,211),width=5);d.polygon([(128,48),(178,77),(171,151),(128,194),(85,151),(78,77)],fill=(13,54,66),outline=(76,164,255),width=3)
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',72);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
except: font=None;small=None
if font:
    bbox=d.textbbox((0,0),'SB',font=font);w=bbox[2]-bbox[0];d.text(((P-w)//2,75),'SB',font=font,fill=(116,247,226),stroke_width=2,stroke_fill=(20,89,105));label='SKYBIT';bbox=d.textbbox((0,0),label,font=small);w=bbox[2]-bbox[0];d.text(((P-w)//2,159),label,font=small,fill=(255,211,91))
for x,y in [(42,42),(211,52),(51,204),(213,196),(32,128),(224,126)]: d.rectangle((x-2,y-2,x+2,y+2),fill=(165,255,245,255))
im.save(ready/'pack.png')
(ready/'SKYBIT-PACK-VERSION.txt').write_text('3.7.0\n',encoding='utf-8')
(ready/'README-SKYBIT.txt').write_text('SKYBIT RESOURCE PACK v3.7.0\nMinecraft Java Edition 1.21.11\nResource Pack Format: 75\n\nVisual Overhaul:\n- kompletne nove material/pixel textury\n- premium Legendary/Mythic crates\n- 3D keys, crystals, gear a armor inventory models\n- SkyBit AFK Zone Core model\n- nove pack branding\n',encoding='utf-8')
(ready/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':75,'description':'§b§lSkyBit Network §8• §fVisual Overhaul §6✦ §7(v3.7.0)'}},indent=2,ensure_ascii=False),encoding='utf-8')
print('textures rebuilt', len(list(texroot.rglob('*.png'))))