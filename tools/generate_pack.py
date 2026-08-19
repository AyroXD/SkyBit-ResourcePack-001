from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json,shutil,zipfile
V='3.4.0'; PF=75; R=Path('build/SkyBit-ResourcePack'); Z=Path(f'SkyBit-ResourcePack-v{V}-READY.zip'); S=Path(f'SkyBit-ResourcePack-v{V}.sha1.txt')
if R.exists(): shutil.rmtree(R)
R.mkdir(parents=True)
P={'basic':('#55f4df','#159b99','#073b4c'),'rare':('#6bb4ff','#285fda','#142f7c'),'epic':('#d17aff','#7938bd','#391968'),'legendary':('#ffd45c','#e78510','#853700'),'vote':('#69ed78','#249b47','#0e5729'),'mythic':('#f27cff','#5d168f','#22052f'),'red':('#ff6b77','#ca3347','#6c1728'),'silver':('#e4edf3','#8999a8','#424d59')}
def C(): return Image.new('RGBA',(64,64),(0,0,0,0))
def poly(d,p,c): d.polygon(p,fill=c)
def item_json(rel):
 q=R/'assets/skybit/items'/f'{rel}.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps({'model':{'type':'minecraft:model','model':f'skybit:item/{rel}'}},indent=2))
def save(im,rel,model=None):
 p=R/'assets/skybit/textures/item'/f'{rel}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p,optimize=True)
 m=R/'assets/skybit/models/item'/f'{rel}.json';m.parent.mkdir(parents=True,exist_ok=True);m.write_text(json.dumps(model or {'parent':'minecraft:item/generated','textures':{'layer0':f'skybit:item/{rel}'}},indent=2));item_json(rel)
def key(t):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im);d.ellipse((7,9,33,35),fill=c);d.ellipse((10,12,30,32),fill=b);d.ellipse((15,17,25,27),fill=(8,14,20,255));poly(d,[(27,20),(55,20),(57,25),(51,30),(44,30),(44,34),(39,34),(39,29),(27,29)],c);poly(d,[(29,22),(51,22),(54,25),(50,27),(42,27),(42,31),(40,31),(40,27),(29,27)],b);d.line((30,22,46,22),fill=a,width=2);return im
def shard(t):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im);poly(d,[(31,5),(49,22),(44,47),(31,58),(13,43),(17,19)],c);poly(d,[(31,9),(44,23),(40,43),(30,53),(18,40),(20,22)],b);poly(d,[(31,10),(31,50),(21,39),(23,22)],a);return im
def crate(t):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im);poly(d,[(10,21),(30,10),(54,20),(33,33)],c);poly(d,[(10,21),(33,33),(33,53),(10,40)],c);poly(d,[(33,33),(54,20),(54,41),(33,53)],b);poly(d,[(13,22),(30,13),(50,21),(33,30)],b);d.line((31,12,33,52),fill='#ffdc74',width=4);d.line((11,31,54,31),fill='#d5aa49',width=4);d.rectangle((29,28,37,37),fill='#75460c');d.rectangle((31,29,35,34),fill=a);return im
def crystal(t):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im);poly(d,[(32,5),(48,24),(43,50),(32,58),(18,47),(15,24)],c);poly(d,[(32,9),(43,25),(39,46),(32,53),(21,44),(20,25)],b);poly(d,[(32,10),(32,52),(23,43),(23,25)],a);return im
def badge(t):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im);poly(d,[(32,7),(39,15),(50,14),(48,27),(55,36),(44,43),(41,55),(32,49),(23,55),(20,43),(9,36),(16,27),(14,14),(25,15)],c);poly(d,[(32,12),(38,20),(45,19),(43,28),(49,35),(40,39),(38,48),(32,44),(26,48),(24,39),(15,35),(21,28),(19,19),(26,20)],b);poly(d,[(32,14),(35,24),(44,24),(37,31),(40,41),(32,35),(24,41),(27,31),(20,24),(29,24)],a);return im
def generic(t='basic',shape='square'):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im)
 if shape=='coin': d.ellipse((9,8,55,55),fill=c);d.ellipse((13,11,51,51),fill=b);d.ellipse((18,16,46,46),fill=a)
 elif shape=='dust':
  for x,y,r in [(20,36,7),(32,24,9),(44,38,7),(31,45,5)]: poly(d,[(x,y-r),(x+r,y),(x,y+r),(x-r,y)],c); poly(d,[(x,y-r+2),(x+r-2,y),(x,y+r-2),(x-r+2,y)],b)
 elif shape=='relic': poly(d,[(32,7),(49,19),(45,43),(32,57),(18,44),(15,20)],c);poly(d,[(32,12),(44,22),(40,40),(32,50),(23,40),(20,23)],b);d.ellipse((25,23,39,37),fill=a)
 else: d.rounded_rectangle((11,11,53,53),radius=9,fill=c,outline=a,width=2);d.rectangle((20,20,44,44),fill=b);d.rectangle((25,25,39,39),fill=a)
 return im
def armor(t,kind):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im)
 if kind=='helmet': poly(d,[(16,17),(24,9),(40,9),(48,17),(47,38),(39,46),(25,46),(17,38)],c);d.rectangle((22,18,42,34),fill=b);d.rectangle((25,21,39,25),fill=a)
 elif kind=='chestplate': poly(d,[(14,13),(25,8),(39,8),(50,13),(45,26),(45,52),(19,52),(19,26)],c);d.rectangle((25,18,39,44),fill=b);d.rectangle((28,21,36,41),fill=a)
 elif kind=='leggings': poly(d,[(18,10),(46,10),(44,31),(39,54),(30,54),(32,31),(25,54),(16,54),(20,31)],c);d.rectangle((23,14,41,29),fill=b);d.rectangle((27,16,37,27),fill=a)
 else: poly(d,[(18,13),(30,13),(30,38),(23,51),(12,51),(18,36)],c);poly(d,[(34,13),(46,13),(46,36),(52,51),(41,51),(34,38)],c);d.rectangle((20,17,27,34),fill=b);d.rectangle((37,17,44,34),fill=b)
 return im
def weapon(t,kind):
 a,b,c=P[t];im=C();d=ImageDraw.Draw(im)
 if kind=='bow': d.arc((8,8,52,56),270,90,fill=c,width=5);d.arc((11,10,49,54),270,90,fill=a,width=2);d.line((48,10,48,54),fill=b,width=2);d.line((47,32,16,32),fill=a,width=3);poly(d,[(12,32),(21,27),(21,37)],a)
 elif kind=='pick': d.line((16,50,41,14),fill=c,width=7);d.line((18,49,42,15),fill=b,width=3);d.arc((15,7,54,30),190,350,fill=a,width=7)
 elif kind=='spear': d.line((17,52,43,11),fill=c,width=6);d.line((19,50,44,12),fill=b,width=3);poly(d,[(43,6),(53,18),(42,20)],a)
 elif kind=='cleaver': d.line((18,51,33,31),fill=c,width=7);poly(d,[(28,8),(53,14),(41,36),(26,30)],c);poly(d,[(31,11),(49,15),(39,31),(29,27)],a)
 else: d.line((17,52,29,37),fill=c,width=7);d.rectangle((20,31,43,38),fill=c);poly(d,[(29,6),(43,12),(37,32),(25,32)],c);poly(d,[(31,9),(40,13),(35,29),(28,29)],a)
 return im
def faces(tex): return {f:{'texture':'#layer0'} for f in ['north','south','east','west','up','down']}
def model3d(rel,kind):
 if kind=='spear': els=[{'from':[7.25,0,7.25],'to':[8.75,13,8.75],'faces':faces('#')},{'from':[5.5,12,5.5],'to':[10.5,16,10.5],'faces':faces('#')}]
 elif kind=='pick': els=[{'from':[7,0,7],'to':[9,13,9],'faces':faces('#')},{'from':[2,11,6.5],'to':[14,15,9.5],'faces':faces('#')}]
 elif kind=='cleaver': els=[{'from':[7,0,7],'to':[9,13,9],'faces':faces('#')},{'from':[3,9,6],'to':[12,16,10],'faces':faces('#')}]
 else: els=[{'from':[7,0,7],'to':[9,5,9],'faces':faces('#')},{'from':[4,4,6.5],'to':[12,6,9.5],'faces':faces('#')},{'from':[6.7,5.5,6.7],'to':[9.3,16,9.3],'faces':faces('#')}]
 return {'textures':{'layer0':f'skybit:item/{rel}'},'elements':els,'display':{'thirdperson_righthand':{'rotation':[0,90,0],'translation':[0,2,1],'scale':[.75,.75,.75]},'firstperson_righthand':{'rotation':[0,-90,20],'translation':[1.2,3.2,1.2],'scale':[.85,.85,.85]},'gui':{'rotation':[30,225,0],'scale':[.9,.9,.9]},'ground':{'translation':[0,3,0],'scale':[.65,.65,.65]},'fixed':{'rotation':[0,180,0],'scale':[1.05,1.05,1.05]}}}
for t in ['basic','rare','epic','legendary','vote','mythic']:
 save(key(t),f'keys/{t}'); save(shard(t),f'fragments/{t}'); save(crate(t),f'crates/{t}',model3d(f'crates/{t}','cleaver'))
 if t!='mythic': save(crystal(t),f'mines/{t}_crystal')
save(generic('legendary','coin'),'currency/skycoin')
for rel,t,sh in [('contracts/daily_contract','basic','square'),('contracts/weekly_contract','epic','square'),('afk/premium_pass','basic','square'),('enchant/arcane_dust','epic','dust'),('enchant/enchant_core','epic','square'),('guilds/guild_seal','basic','square'),('bounty/bounty_token','red','square'),('treasure/treasure_compass','legendary','square'),('events/supply_beacon','rare','square'),('relics/relic_shard','epic','relic'),('relics/prosperity','legendary','relic'),('relics/wisdom','rare','relic'),('relics/fortune','vote','relic'),('relics/titan','red','relic'),('relics/voyager','basic','relic'),('achievements/medal','legendary','square'),('collections/token','basic','square'),('cozy/hearty_stew','legendary','square')]: save(generic(t,sh),rel)
for t,n in [('basic','vip'),('rare','knight'),('epic','baron'),('legendary','king'),('red','emperor')]: save(badge(t),f'vip/{n}_badge')
for t,n in [('basic','miner'),('red','hunter'),('rare','fisher'),('vote','farmer'),('legendary','woodcutter')]: save(badge(t),f'professions/{n}')
for t,n in [('legendary','bronze'),('silver','silver'),('legendary','gold'),('rare','platinum'),('epic','master')]: save(badge(t),f'renown/{n}')
for n,t in [('menu','basic'),('profile','rare'),('settings','silver'),('questhub','legendary'),('leaderboard','epic'),('booster','vote'),('serverpass','legendary'),('links','basic')]: save(generic(t),f'ui/{n}')
for n,t,k in [('skyfang_blade','rare','blade'),('ember_cleaver','epic','cleaver'),('stormcaller_spear','rare','spear'),('void_reaver','mythic','blade')]:
 rel=f'gear/weapons/{n}';save(weapon(t,k),rel,model3d(rel,k))
rel='gear/weapons/frostbite_bow';save(weapon('rare','bow'),rel,{'parent':'minecraft:item/handheld','textures':{'layer0':f'skybit:item/{rel}'}})
rel='gear/tools/titan_pickaxe';save(weapon('legendary','pick'),rel,model3d(rel,'pick'))
for setn,t in [('stormguard','rare'),('emberforged','epic'),('voidwarden','mythic')]:
 for kind in ['helmet','chestplate','leggings','boots']: save(armor(t,kind),f'gear/armor/{setn}_{kind}')
W=R/'assets/minecraft/textures/gui/sprites/widget';W.mkdir(parents=True,exist_ok=True)
def btn(state):
 im=Image.new('RGBA',(200,20),(0,0,0,0));d=ImageDraw.Draw(im);cs={'normal':('#0b2330','#45d8c2'),'highlighted':('#0f3542','#7bffe7'),'disabled':('#121a20','#44535a')}[state];d.rounded_rectangle((1,1,198,18),radius=3,fill=cs[0],outline=cs[1],width=2);return im
for st,n,b in [('normal','button.png',3),('highlighted','button_highlighted.png',3),('disabled','button_disabled.png',1)]: btn(st).save(W/n);(W/(n+'.mcmeta')).write_text(json.dumps({'gui':{'scaling':{'type':'nine_slice','width':200,'height':20,'border':b}}}))
langs={'sk_sk':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ SPÄŤ DO HRY','menu.disconnect':'§c✖ ODPOJIŤ SA','menu.options':'§e⚙ NASTAVENIA','menu.server_links':'§b✦ SKYBIT ODKAZY ✦','menu.serverLinks':'§b✦ SKYBIT ODKAZY ✦','menu.advancements':'§d★ ACHIEVEMENTY','menu.stats':'§b▣ ŠTATISTIKY'},'cs_cz':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ ZPĚT DO HRY','menu.disconnect':'§c✖ ODPOJIT SE','menu.options':'§e⚙ NASTAVENÍ'},'en_us':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ BACK TO SKYBIT','menu.disconnect':'§c✖ LEAVE SKYBIT','menu.options':'§e⚙ SETTINGS'}}
for loc,d in langs.items(): q=R/'assets/minecraft/lang'/f'{loc}.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(d,ensure_ascii=False,indent=2))
logo=Image.new('RGBA',(128,128),(7,19,28,255));d=ImageDraw.Draw(logo);d.rounded_rectangle((12,12,116,116),radius=24,fill='#0f3542',outline='#51e4cf',width=6);d.text((38,49),'SB',fill='#a8fff1');logo.save(R/'pack.png')
(R/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':PF,'description':'§b§lSkyBit Network §8• §fCustom Gear & Crates §7(v3.4.0)'}},ensure_ascii=False,indent=2));(R/'SKYBIT-PACK-VERSION.txt').write_text(V+'\n');(R/'README-SKYBIT.txt').write_text('SkyBit Resource Pack v3.4.0\nMinecraft Java 1.21.11\nCustom Gear, 3D Weapons, Mythic Crate, Pause UI\n')
if Z.exists(): Z.unlink()
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(R.rglob('*')):
  if f.is_file(): z.write(f,f.relative_to(R))
sha=hashlib.sha1(Z.read_bytes()).hexdigest();S.write_text(sha+'\n');print('Created',Z,'SHA1='+sha)
