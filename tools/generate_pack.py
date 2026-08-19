from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, shutil, zipfile

VERSION = '3.2.0'
PACK_FORMAT = 75
ROOT = Path('build/SkyBit-ResourcePack')
ZIP = Path(f'SkyBit-ResourcePack-v{VERSION}-READY.zip')
SHA = Path(f'SkyBit-ResourcePack-v{VERSION}.sha1.txt')
S = 64

if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)

PALETTE = {
    'basic': ('#55f4df','#159b99','#073b4c'),
    'rare': ('#6bb4ff','#285fda','#142f7c'),
    'epic': ('#d17aff','#7938bd','#391968'),
    'legendary': ('#ffd45c','#e78510','#853700'),
    'vote': ('#69ed78','#249b47','#0e5729'),
    'red': ('#ff6b77','#ca3347','#6c1728'),
    'silver': ('#e4edf3','#8999a8','#424d59'),
}

def canvas(): return Image.new('RGBA',(S,S),(0,0,0,0))
def poly(d,pts,fill,outline=None,w=1):
    d.polygon(pts,fill=fill)
    if outline: d.line(pts+[pts[0]],fill=outline,width=w,joint='curve')

def save_item(img, rel):
    tex=ROOT/'assets/skybit/textures/item'/f'{rel}.png'; tex.parent.mkdir(parents=True,exist_ok=True); img.save(tex,optimize=True)
    model=ROOT/'assets/skybit/models/item'/f'{rel}.json'; model.parent.mkdir(parents=True,exist_ok=True)
    model.write_text(json.dumps({'parent':'minecraft:item/generated','textures':{'layer0':f'skybit:item/{rel}'}},indent=2),encoding='utf-8')
    item=ROOT/'assets/skybit/items'/f'{rel}.json'; item.parent.mkdir(parents=True,exist_ok=True)
    item.write_text(json.dumps({'model':{'type':'minecraft:model','model':f'skybit:item/{rel}'}},indent=2),encoding='utf-8')

def key(tier):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im)
    d.ellipse((11,46,56,56),fill=(0,0,0,80)); d.ellipse((7,9,33,35),fill=dark); d.ellipse((10,12,30,32),fill=mid); d.ellipse((15,17,25,27),fill=(10,18,24,255))
    d.polygon([(27,20),(52,20),(57,25),(52,30),(46,30),(46,35),(40,35),(40,30),(27,30)],fill=dark)
    d.polygon([(29,22),(51,22),(54,25),(51,27),(44,27),(44,32),(42,32),(42,27),(29,27)],fill=mid)
    d.rectangle((30,22,46,23),fill=light); d.rectangle((12,13,20,15),fill=light); d.rectangle((8,6,12,10),fill=(255,255,255,230))
    return im

def shard(tier):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im); d.ellipse((13,49,52,57),fill=(0,0,0,75))
    poly(d,[(31,5),(49,22),(44,47),(31,58),(13,43),(17,19)],dark); poly(d,[(31,9),(44,23),(40,43),(30,53),(18,40),(20,22)],mid)
    d.polygon([(31,10),(31,50),(21,39),(23,22)],fill=light); d.polygon([(32,12),(40,23),(36,31),(32,34)],fill=(255,255,255,175))
    return im

def crate(tier):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im); d.ellipse((8,49,56,58),fill=(0,0,0,85))
    poly(d,[(10,21),(30,10),(54,20),(33,33)],dark); poly(d,[(10,21),(33,33),(33,53),(10,40)],dark); poly(d,[(33,33),(54,20),(54,41),(33,53)],mid); poly(d,[(13,22),(30,13),(50,21),(33,30)],mid)
    d.line((31,12,33,52),fill='#ffdc74',width=4); d.line((11,31,54,31),fill='#d5aa49',width=4); d.rectangle((29,28,37,37),fill='#75460c'); d.rectangle((31,29,35,34),fill='#ffe589'); d.line((17,21,30,15),fill=light,width=2)
    return im

def crystal(tier):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im); d.ellipse((13,51,51,58),fill=(0,0,0,90))
    poly(d,[(32,5),(48,24),(43,50),(32,58),(18,47),(15,24)],dark); poly(d,[(32,9),(43,25),(39,46),(32,53),(21,44),(20,25)],mid)
    d.polygon([(32,10),(32,52),(23,43),(23,25)],fill=light); d.polygon([(33,12),(40,25),(36,31),(33,36)],fill=(255,255,255,175)); return im

def badge(tier):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im); d.ellipse((15,50,49,56),fill=(0,0,0,75))
    poly(d,[(32,7),(39,15),(50,14),(48,27),(55,36),(44,43),(41,55),(32,49),(23,55),(20,43),(9,36),(16,27),(14,14),(25,15)],dark)
    poly(d,[(32,11),(38,19),(45,18),(43,28),(49,35),(40,39),(38,48),(32,44),(26,48),(24,39),(15,35),(21,28),(19,18),(26,19)],mid)
    d.polygon([(32,13),(35,24),(44,24),(37,31),(40,41),(32,35),(24,41),(27,31),(20,24),(29,24)],fill=light); return im

def simple(kind,tier='basic'):
    light,mid,dark=PALETTE[tier]; im=canvas(); d=ImageDraw.Draw(im); d.ellipse((12,50,52,57),fill=(0,0,0,70))
    if kind=='coin':
        d.ellipse((9,8,55,55),fill='#6f3a00'); d.ellipse((12,9,52,52),fill='#e48e0b'); d.ellipse((16,13,48,48),fill='#ffc83d'); d.arc((20,16,44,43),35,325,fill='#fff1a6',width=3); d.polygon([(37,17),(25,18),(21,26),(34,27),(29,32),(20,31),(17,38),(32,39),(43,28),(30,27)],fill='#7a4300')
    elif kind=='dust':
        for x,y,r in [(20,35,7),(32,24,9),(43,38,8),(30,43,5)]: d.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=dark); d.polygon([(x,y-r+2),(x+r-2,y),(x,y+r-2),(x-r+2,y)],fill=mid)
    elif kind=='compass':
        d.ellipse((10,10,54,54),fill=dark); d.ellipse((14,14,50,50),fill='#152431'); d.ellipse((18,18,46,46),outline=mid,width=3); d.polygon([(32,16),(37,31),(32,28),(27,31)],fill=light); d.polygon([(32,48),(27,33),(32,36),(37,33)],fill='#ff5d63')
    elif kind=='beacon':
        d.polygon([(32,7),(48,20),(44,48),(32,57),(20,48),(16,20)],fill=dark); d.polygon([(32,11),(43,23),(39,44),(32,51),(25,44),(21,23)],fill=mid); d.rectangle((29,18,35,42),fill=light); d.rectangle((24,27,40,33),fill=light)
    elif kind=='seal':
        d.ellipse((13,11,51,49),fill=dark); d.ellipse((17,15,47,45),fill=mid); d.polygon([(32,18),(39,27),(36,39),(28,39),(25,27)],fill=light); d.rectangle((29,25,35,34),fill='#10232c'); d.polygon([(22,43),(17,58),(29,50),(32,57),(35,49),(48,57),(43,43)],fill=dark)
    elif kind=='token':
        d.ellipse((12,11,52,51),fill=dark); d.ellipse((16,15,48,47),fill=mid); d.polygon([(32,18),(37,28),(47,29),(39,36),(41,46),(32,40),(23,46),(25,36),(17,29),(27,28)],fill=light)
    elif kind=='relic':
        d.polygon([(32,7),(49,19),(45,43),(32,57),(18,44),(15,20)],fill=dark); d.polygon([(32,12),(44,22),(40,40),(32,50),(23,40),(20,23)],fill=mid); d.ellipse((25,23,39,37),fill=light); d.ellipse((29,27,35,33),fill='#10242e')
    elif kind=='medal':
        d.polygon([(20,8),(29,8),(34,26),(26,30)],fill='#3e5e9b'); d.polygon([(35,8),(44,8),(38,30),(30,26)],fill='#d3525f'); d.ellipse((17,24,47,54),fill=dark); d.ellipse((21,28,43,50),fill=mid); d.polygon([(32,31),(35,38),(42,39),(37,44),(39,50),(32,46),(25,50),(27,44),(22,39),(29,38)],fill=light)
    elif kind=='food':
        d.ellipse((11,28,53,52),fill=dark); d.ellipse((14,26,50,48),fill='#d86b34'); d.ellipse((17,27,47,44),fill='#f0b45e'); d.ellipse((21,30,28,36),fill='#60c868'); d.ellipse((34,31,42,38),fill='#b33e35'); d.rectangle((12,47,52,51),fill=dark)
    else:
        d.rounded_rectangle((12,12,52,52),radius=8,fill=dark,outline=light,width=2); d.rectangle((20,20,44,44),fill=mid); d.rectangle((24,24,40,40),fill=light)
    return im

def scroll(accent):
    im=canvas(); d=ImageDraw.Draw(im); d.ellipse((12,51,53,57),fill=(0,0,0,65)); d.rounded_rectangle((14,8,50,52),radius=7,fill='#5b3b22'); d.rounded_rectangle((17,10,47,50),radius=5,fill='#ead5a6'); d.rectangle((20,17,44,20),fill=accent)
    for y,w in [(25,20),(30,24),(35,18),(40,21)]: d.rectangle((20,y,20+w,y+2),fill='#7d674a')
    d.ellipse((38,39,49,50),fill='#6d173d'); d.ellipse((40,41,47,48),fill=accent); return im

for t in ['basic','rare','epic','legendary','vote']:
    save_item(key(t),f'keys/{t}'); save_item(shard(t),f'fragments/{t}'); save_item(crate(t),f'crates/{t}'); save_item(crystal(t),f'mines/{t}_crystal')
save_item(simple('coin','legendary'),'currency/skycoin')
save_item(scroll('#48e4d1'),'contracts/daily_contract'); save_item(scroll('#d46cff'),'contracts/weekly_contract')
save_item(simple('token','basic'),'afk/premium_pass')
for t,name in [('basic','vip'),('rare','knight'),('epic','baron'),('legendary','king'),('red','emperor')]: save_item(badge(t),f'vip/{name}_badge')

extra = {
'enchant/arcane_dust':('dust','epic'),'enchant/enchant_core':('beacon','epic'),'guilds/guild_seal':('seal','basic'),'bounty/bounty_token':('token','red'),'treasure/treasure_compass':('compass','legendary'),'events/supply_beacon':('beacon','rare'),'relics/relic_shard':('relic','epic'),'relics/prosperity':('relic','legendary'),'relics/wisdom':('relic','rare'),'relics/fortune':('relic','vote'),'relics/titan':('relic','red'),'relics/voyager':('relic','basic'),'achievements/medal':('medal','legendary'),'collections/token':('token','basic'),'cozy/hearty_stew':('food','legendary')}
for rel,(kind,tier) in extra.items(): save_item(simple(kind,tier),rel)
for tier,name in [('basic','miner'),('red','hunter'),('rare','fisher'),('vote','farmer'),('legendary','woodcutter')]: save_item(badge(tier),f'professions/{name}')
for tier,name in [('legendary','bronze'),('silver','silver'),('legendary','gold'),('rare','platinum'),('epic','master')]: save_item(badge(tier),f'renown/{name}')
for name,tier in [('menu','basic'),('profile','rare'),('settings','silver'),('questhub','legendary'),('leaderboard','epic'),('booster','vote'),('serverpass','legendary'),('links','basic')]: save_item(simple('generic',tier),f'ui/{name}')

widget=ROOT/'assets/minecraft/textures/gui/sprites/widget'; widget.mkdir(parents=True,exist_ok=True)
def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def button(state):
    im=Image.new('RGBA',(200,20),(0,0,0,0)); d=ImageDraw.Draw(im)
    if state=='normal': c1,c2,border,inner='#0b2330','#103b43','#45d8c2','#1c6b72'
    elif state=='highlighted': c1,c2,border,inner='#0f3542','#12666b','#7bffe7','#38b8c3'
    else: c1,c2,border,inner='#121a20','#1c272e','#44535a','#2b383f'
    a,b=rgb(c1),rgb(c2)
    for y in range(2,18):
        t=(y-2)/15; col=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)); d.line((2,y,197,y),fill=col+(255,))
    d.rectangle((1,1,198,18),outline=border,width=1); d.rectangle((3,3,196,16),outline=inner,width=1); d.rectangle((0,5,1,14),fill=border); d.rectangle((198,5,199,14),fill=border)
    if state=='highlighted': d.line((5,4,194,4),fill='#a8fff1',width=1)
    return im
for state,name,border in [('normal','button.png',3),('highlighted','button_highlighted.png',3),('disabled','button_disabled.png',1)]:
    button(state).save(widget/name,optimize=True); (widget/(name+'.mcmeta')).write_text(json.dumps({'gui':{'scaling':{'type':'nine_slice','width':200,'height':20,'border':border}}},indent=2),encoding='utf-8')

langs={
'sk_sk':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ SPÄŤ DO HRY','menu.disconnect':'§c✖ ODPOJIŤ SA','menu.options':'§e⚙ NASTAVENIA','menu.server_links':'§b✦ SKYBIT ODKAZY ✦','menu.serverLinks':'§b✦ SKYBIT ODKAZY ✦','menu.advancements':'§d★ ACHIEVEMENTY','menu.stats':'§b▣ ŠTATISTIKY','menu.feedback':'§a✎ SPÄTNÁ VÄZBA','menu.reportBugs':'§c⚠ NAHLÁSIŤ PROBLÉM','menu.playerReporting':'§c⚠ REPORT HRÁČA'},
'cs_cz':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ ZPĚT DO HRY','menu.disconnect':'§c✖ ODPOJIT SE','menu.options':'§e⚙ NASTAVENÍ','menu.server_links':'§b✦ SKYBIT ODKAZY ✦','menu.serverLinks':'§b✦ SKYBIT ODKAZY ✦','menu.advancements':'§d★ ACHIEVEMENTY','menu.stats':'§b▣ STATISTIKY'},
'en_us':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ BACK TO SKYBIT','menu.disconnect':'§c✖ LEAVE SKYBIT','menu.options':'§e⚙ SETTINGS','menu.server_links':'§b✦ SKYBIT LINKS ✦','menu.serverLinks':'§b✦ SKYBIT LINKS ✦','menu.advancements':'§d★ ACHIEVEMENTS','menu.stats':'§b▣ STATISTICS'}}
for loc,data in langs.items():
    p=ROOT/'assets/minecraft/lang'/f'{loc}.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

logo=Image.new('RGBA',(128,128),(7,19,28,255)); d=ImageDraw.Draw(logo)
for r,c in [(55,'#0b3240'),(47,'#0f5560'),(38,'#133b4a')]: d.ellipse((64-r,64-r,64+r,64+r),fill=c)
d.polygon([(64,18),(99,38),(99,79),(64,108),(29,79),(29,38)],fill='#0b2430',outline='#51e4cf'); d.polygon([(64,27),(90,42),(90,73),(64,95),(38,73),(38,42)],fill='#103c49')
d.rectangle((46,44,68,51),fill='#66f5df'); d.rectangle((46,50,53,64),fill='#66f5df'); d.rectangle((46,61,67,68),fill='#66f5df'); d.rectangle((61,67,68,80),fill='#66f5df'); d.rectangle((46,77,68,84),fill='#66f5df')
d.rectangle((72,44,79,84),fill='#62aaff'); d.rectangle((79,44,88,51),fill='#62aaff'); d.rectangle((79,61,88,68),fill='#62aaff'); d.rectangle((79,77,88,84),fill='#62aaff'); d.rectangle((87,51,94,61),fill='#62aaff'); d.rectangle((87,68,94,77),fill='#62aaff')
logo.save(ROOT/'pack.png',optimize=True)
(ROOT/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':PACK_FORMAT,'description':'§b§lSkyBit Network §8• §fPremium Resources §7(v3.2.0)'}},indent=2,ensure_ascii=False),encoding='utf-8')
(ROOT/'SKYBIT-PACK-VERSION.txt').write_text(VERSION+'\n',encoding='utf-8')
(ROOT/'SKYBIT-UI-THEME.txt').write_text('SkyBit UI Theme v3.2.0\nMinecraft Java 1.21.11\nPack format 75\n',encoding='utf-8')
(ROOT/'server.properties.example.txt').write_text('resource-pack=https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.2.0-READY.zip\nresource-pack-sha1=<SHA1_FROM_FILE>\nrequire-resource-pack=false\n',encoding='utf-8')

if ZIP.exists(): ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(ROOT.rglob('*')):
        if f.is_file(): z.write(f,f.relative_to(ROOT))
sha=hashlib.sha1(ZIP.read_bytes()).hexdigest(); SHA.write_text(sha+'\n',encoding='utf-8')
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None and 'pack.mcmeta' in z.namelist() and 'pack.png' in z.namelist()
print(f'Created {ZIP} ({ZIP.stat().st_size} bytes) SHA1={sha}')
