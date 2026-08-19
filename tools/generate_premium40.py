from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,random,shutil
V='4.0.0';PF=75;R=Path('build/SkyBit-ResourcePack')
if R.exists():shutil.rmtree(R)
R.mkdir(parents=True)
P={
'basic':('#061c23','#08717b','#18d8d1','#b9fff8','#a7bcc0','#45fff1'),'rare':('#071a3f','#164c9a','#1f8dff','#d8ebff','#b6c9e4','#63b8ff'),'epic':('#22072f','#641e82','#b732ef','#f1c8ff','#bda3ca','#dc6cff'),'legendary':('#3b1c01','#9a5207','#ffad12','#fff0a6','#d8b46a','#ffd35c'),'mythic':('#250610','#82132d','#ef234f','#ffd0da','#b7a8ae','#ff4d80'),'vote':('#082610','#2d7b3d','#54d86a','#dbffe1','#a9c4ae','#87ff97'),'silver':('#182029','#4c5e6e','#9eafbd','#edf6ff','#cbd5dc','#ffffff'),'ember':('#2d0a05','#8f2a11','#f45b21','#ffd397','#a96d50','#ff974f'),'storm':('#061d2a','#0f6477','#24c9df','#c8fbff','#91b6c1','#70f1ff'),'void':('#14091d','#452052','#9a45bd','#f0c9ff','#8b7b96','#d073f3'),'gold':('#3a2402','#8d610b','#eeb632','#fff0a2','#c3a55e','#ffe66d'),'neutral':('#0b1218','#2c3945','#657784','#e4edf2','#96a5ae','#b9d9e6')}
def rgb(h):h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in(0,2,4))
def C(t):return [rgb(x)+(255,) for x in P[t]]
def im():return Image.new('RGBA',(64,64),(0,0,0,0))
def sh(d):d.ellipse((9,52,55,58),fill=(0,0,0,80))
def poly(d,p,f,o=None):d.polygon(p,fill=f);o and d.line(p+[p[0]],fill=o,width=1)
def sparkle(d,c):
 for x,y in[(10,18),(52,15),(12,45),(52,46)]:d.point((x,y),fill=c);d.point((x+1,y),fill=c[:3]+(100,))
def badge(t,r='vip'):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);poly(d,[(20,37),(27,42),(25,56),(18,51)],c[1]);poly(d,[(44,37),(37,42),(39,56),(46,51)],c[1]);poly(d,[(17,13),(25,8),(39,8),(47,13),(46,35),(32,49),(18,35)],c[0],c[4]);poly(d,[(21,16),(27,12),(37,12),(43,16),(42,33),(32,43),(22,33)],c[1],c[3]);poly(d,[(32,15),(39,22),(32,31),(25,22)],c[2],c[3]);poly(d,[(32,17),(36,22),(32,27),(28,22)],c[5]);
 if r=='knight':d.rectangle((25,32,39,39),fill=c[0],outline=c[4]);d.line((26,34,38,34),fill=c[3])
 elif r=='baron':poly(d,[(23,35),(26,28),(31,33),(35,27),(41,35),(39,39),(25,39)],c[2],c[3])
 elif r=='king':poly(d,[(21,13),(25,5),(30,11),(32,4),(35,11),(40,5),(44,13)],c[2],c[3])
 elif r=='emperor':poly(d,[(18,14),(21,5),(27,12),(32,3),(37,12),(43,5),(46,14)],c[2],c[3])
 else:d.line((24,36,40,36),fill=c[5],width=2)
 sparkle(d,c[5]);return a
def key(t):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);d.line((15,47,42,24),fill=c[0],width=9);d.line((15,45,42,22),fill=c[4],width=6);d.line((17,43,41,22),fill=c[3],width=2);d.rounded_rectangle((32,8,55,31),5,fill=c[0],outline=c[4],width=3);d.rounded_rectangle((36,12,51,27),3,fill=c[1],outline=c[3],width=2);poly(d,[(43,14),(49,20),(43,26),(37,20)],c[2],c[5]);d.rectangle((9,42,13,49),fill=c[4]);d.rectangle((15,46,19,53),fill=c[4]);sparkle(d,c[5]);return a
def crate(t):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);poly(d,[(9,24),(31,13),(55,23),(33,36)],c[0],c[4]);poly(d,[(9,24),(33,36),(33,54),(9,42)],c[1],c[4]);poly(d,[(33,36),(55,23),(55,43),(33,54)],c[0],c[4]);poly(d,[(12,23),(31,15),(52,23),(33,33)],c[2],c[3]);d.line((31,15,33,54),fill=c[4],width=4);d.line((10,33,55,33),fill=c[4],width=3);d.rectangle((28,30,38,41),fill=c[0],outline=c[3],width=2);poly(d,[(33,31),(37,35),(33,40),(29,35)],c[2],c[5]);
 if t=='legendary':
  for x in(19,31,43):poly(d,[(x,15),(x+3,8),(x+6,16)],c[2],c[3])
 if t=='mythic':poly(d,[(12,22),(6,14),(14,17)],c[2],c[5]);poly(d,[(51,22),(58,14),(50,17)],c[2],c[5]);poly(d,[(27,14),(32,5),(37,14)],c[2],c[3])
 sparkle(d,c[5]);return a
def gem(t):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);poly(d,[(32,5),(48,20),(43,45),(32,57),(16,44),(18,20)],c[0],c[4]);poly(d,[(32,9),(43,22),(39,42),(32,51),(22,40),(22,22)],c[1]);poly(d,[(32,10),(32,49),(24,39),(24,23)],c[2]);poly(d,[(33,12),(40,23),(36,30),(33,34)],c[3]);sparkle(d,c[5]);return a
def coin(t):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);d.ellipse((10,8,54,52),fill=c[0],outline=c[4],width=3);d.ellipse((15,13,49,47),fill=c[1],outline=c[3],width=2);d.ellipse((20,18,44,42),fill=c[2]);poly(d,[(32,21),(40,30),(32,40),(24,30)],c[0],c[3]);poly(d,[(32,24),(36,30),(32,36),(28,30)],c[5]);return a
def card(t,star=False):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);d.rounded_rectangle((8,14,56,47),6,fill=c[0],outline=c[4],width=3);d.rounded_rectangle((13,18,51,43),4,fill=c[1],outline=c[3]);poly(d,[(22,23),(29,31),(22,39),(15,31)],c[2],c[5]);
 if star:poly(d,[(41,22),(44,28),(50,28),(45,32),(47,39),(41,35),(35,39),(37,32),(32,28),(38,28)],c[2],c[3])
 else:d.rectangle((36,25,47,28),fill=c[5]);d.rectangle((36,34,44,37),fill=c[2])
 return a
def core(t):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);poly(d,[(32,5),(49,18),(45,47),(32,58),(18,47),(15,18)],c[0],c[4]);poly(d,[(32,10),(43,22),(39,43),(32,50),(24,42),(21,22)],c[1]);d.rectangle((29,17,35,44),fill=c[2],outline=c[3]);d.rectangle((22,28,42,34),fill=c[2],outline=c[3]);d.rectangle((30,20,34,32),fill=c[5]);sparkle(d,c[5]);return a
def ui(t,s):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d);d.rounded_rectangle((8,8,56,56),9,fill=c[0],outline=c[4],width=3);d.rounded_rectangle((13,13,51,51),7,fill=c[1],outline=c[3]);
 if s=='profile':d.ellipse((25,17,39,31),fill=c[2]);d.ellipse((18,32,46,49),fill=c[2])
 elif s=='settings':d.ellipse((21,21,43,43),outline=c[2],width=6);d.ellipse((28,28,36,36),fill=c[3])
 elif s=='leaderboard':d.rectangle((18,33,25,47),fill=c[2]);d.rectangle((29,23,36,47),fill=c[5]);d.rectangle((40,29,47,47),fill=c[3])
 elif s=='links':d.arc((15,23,34,42),80,280,fill=c[2],width=4);d.arc((30,23,49,42),260,100,fill=c[3],width=4);d.line((27,32,37,32),fill=c[5],width=4)
 elif s=='menu':
  for y in(20,30,40):d.rectangle((19,y,45,y+4),fill=c[2])
 else:poly(d,[(32,15),(39,27),(48,31),(39,35),(32,49),(25,35),(16,31),(25,27)],c[2],c[3])
 return a
def weapon(t,k):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d)
 if k=='bow':d.arc((8,7,51,57),270,90,fill=c[4],width=5);d.arc((11,9,48,55),270,90,fill=c[2],width=2);d.line((48,10,48,54),fill=c[3]);d.line((47,32,16,32),fill=c[5],width=3);poly(d,[(12,32),(21,27),(21,37)],c[3])
 elif k=='pick':d.line((17,52,42,16),fill=(103,67,41,255),width=7);d.arc((15,7,55,31),190,350,fill=c[2],width=8)
 elif k=='spear':d.line((16,53,43,13),fill=(115,75,42,255),width=6);poly(d,[(44,5),(55,18),(42,21)],c[2],c[3])
 elif k=='cleaver':d.line((18,53,33,33),fill=(111,70,39,255),width=7);poly(d,[(27,7),(54,14),(42,37),(25,31)],c[0],c[4]);poly(d,[(31,10),(50,15),(39,32),(29,28)],c[2],c[3])
 else:d.line((17,53,29,39),fill=(111,70,39,255),width=7);d.rectangle((20,32,44,39),fill=c[4]);poly(d,[(29,5),(44,12),(37,33),(24,33)],c[0],c[4]);poly(d,[(31,9),(40,13),(35,29),(28,29)],c[2],c[3])
 sparkle(d,c[5]);return a
def armor(t,p):
 c=C(t);a=im();d=ImageDraw.Draw(a);sh(d)
 if p=='helmet':poly(d,[(15,17),(24,8),(40,8),(49,17),(47,39),(39,47),(25,47),(17,39)],c[0],c[4]);d.rectangle((22,18,42,35),fill=c[1],outline=c[3]);d.rectangle((25,22,39,26),fill=c[2])
 elif p=='chestplate':poly(d,[(13,14),(24,8),(40,8),(51,14),(46,27),(46,53),(18,53),(18,27)],c[0],c[4]);d.rectangle((25,19,39,45),fill=c[1]);d.rectangle((28,22,36,42),fill=c[2])
 elif p=='leggings':poly(d,[(17,10),(47,10),(45,32),(40,55),(31,55),(32,32),(26,55),(16,55),(20,32)],c[0],c[4]);d.rectangle((23,14,41,30),fill=c[1]);d.rectangle((27,17,37,28),fill=c[2])
 else:poly(d,[(17,14),(30,14),(30,39),(23,52),(11,52),(17,37)],c[0],c[4]);poly(d,[(34,14),(47,14),(47,37),(53,52),(41,52),(34,39)],c[0],c[4]);d.rectangle((20,18,27,35),fill=c[2]);d.rectangle((37,18,44,35),fill=c[2])
 return a
def atlas(t):
 c=C(t);a=Image.new('RGBA',(64,64));d=ImageDraw.Draw(a);q=random.Random(t)
 for i in range(16):
  x=i%4*16;y=i//4*16;z=c[i%6];d.rectangle((x,y,x+15,y+15),fill=z);d.line((x,y,x+15,y),fill=tuple(min(255,v+20) for v in z[:3])+(255,));d.line((x,y+15,x+15,y+15),fill=tuple(max(0,v-25) for v in z[:3])+(255,));
  for _ in range(4):d.point((x+q.randint(2,13),y+q.randint(2,13)),fill=c[(i+2)%6])
 return a
def face(i):x=i%4*4;y=i//4*4;u=[x,y,x+4,y+4];return{k:{'uv':u,'texture':'#layer0'}for k in('north','south','east','west','up','down')}
def cube(a,b,c,d,e,f,i=1):return{'from':[a,b,c],'to':[d,e,f],'faces':face(i)}
def geo(k,v=''):
 if k=='crate':
  e=[cube(2.5,1,2.5,13.5,8.2,13.5,0),cube(2,8.2,2,14,12.5,14,1),cube(2.7,3.4,2,13.3,4.8,3.4,4),cube(6.8,4.2,1.4,9.2,8.8,3.8,3)]
  if v=='legendary':e += [cube(4.2,12.3,6.8,5.9,15.1,9.2,3),cube(7.1,12.4,6.7,8.9,15.8,9.3,3),cube(10.1,12.3,6.8,11.8,15.1,9.2,3)]
  if v=='mythic':e += [cube(.7,7.8,6.1,3,12.8,9.9,7),cube(13,7.8,6.1,15.3,12.8,9.9,7),cube(5.5,12.2,6.1,7.1,15.8,9.9,6),cube(8.9,12.2,6.1,10.5,15.8,9.9,6)]
  return'crate',e
 if k=='key':return'small',[cube(7,0,7,9.2,10.6,9,4),cube(4.6,9.5,7,11.6,12.2,9,1),cube(4.6,6.2,7,7,9.6,9,1),cube(9.2,6.2,7,11.6,9.6,9,2),cube(7,0,7,10.5,2.2,9,3)]
 if k in('gem','core'):return'small',[cube(7,2,7,9,11.8,9,1),cube(5.6,5,7,7,9,9,0),cube(9,6.2,7,10.4,10.2,9,2),cube(7.2,11.8,7.2,8.8,15.1,8.8,6)]
 if k=='badge':return'small',[cube(4.7,4,6.7,11.3,10.2,9.3,1),cube(6.1,10.1,7,7.8,14.7,9,3),cube(8.2,10.1,7,9.9,14.7,9,3),cube(5.7,5,6.1,10.3,9.2,9.9,6)]
 if k=='coin':return'small',[cube(4,4,7,12,12,9,1),cube(5.2,5.2,6.4,10.8,10.8,9.6,3),cube(6.5,6.5,5.8,9.5,9.5,10.2,6)]
 if k=='card':return'small',[cube(3.2,5,7,12.8,11,9,1),cube(5,10.6,7,6.8,12.4,9,3),cube(9.2,10.6,7,11,12.4,9,3)]
 if k=='weapon':
  if v=='spear':e=[cube(7,0,7,9,2,9,4),cube(7.25,2,7.25,8.75,13.2,8.75,4),cube(6.1,12.5,6.8,9.9,13.6,9.2,3),cube(6.9,13.2,6.9,9.1,15.2,9.1,1)]
  elif v=='pick':e=[cube(6.8,0,6.8,9.2,2,9.2,4),cube(7.1,2,7.1,8.9,12.7,8.9,4),cube(3.1,11,6.3,12.9,13.6,9.7,1),cube(2,12.3,6.1,4,15,9.9,2)]
  elif v=='cleaver':e=[cube(6.7,0,6.7,9.3,2,9.3,4),cube(7.1,2,7.1,8.9,12.8,8.9,4),cube(6.2,9.4,6,11.8,14.6,10,1),cube(3.6,8.3,6,6.2,14.1,10,2)]
  elif v=='bow':e=[cube(4.8,2,7.2,6.2,14,8.8,1),cube(10.8,2,7.2,12.2,14,8.8,1),cube(8,2,7.75,8.35,14,8.25,6)]
  else:e=[cube(6.4,0,6.4,9.6,2,9.6,4),cube(7,2,7,9,6.4,9,4),cube(4.6,6.1,6.25,11.4,7.4,9.75,3),cube(7.1,7.4,7.1,8.9,16,8.9,1)]
  return'weapon',e
 if k=='armor':
  if v=='helmet':e=[cube(4.8,5,5.2,11.2,11.4,10.8,1),cube(5.4,4.1,5.7,10.6,6,10.3,0)]
  elif v=='chestplate':e=[cube(5.2,4,6.3,10.8,12,9.7,1),cube(2.8,5,6.5,5.2,9.8,9.5,2),cube(10.8,5,6.5,13.2,9.8,9.5,2)]
  elif v=='leggings':e=[cube(4.8,9,6.5,11.2,12,9.5,1),cube(5,3,6.6,7.5,9.3,9.4,1),cube(8.5,3,6.6,11,9.3,9.4,1)]
  else:e=[cube(4.5,3,6.4,7.5,7.5,9.6,1),cube(8.5,3,6.4,11.5,7.5,9.6,1)]
  return'small',e
 return'small',[cube(5,4,6,11,12,10,1),cube(6.2,6,5.4,9.8,10,10.6,6)]
def disp(k):
 if k=='weapon':return{'thirdperson_righthand':{'rotation':[0,92,0],'translation':[0,2.2,1],'scale':[.82]*3},'firstperson_righthand':{'rotation':[0,-90,24],'translation':[1.3,3.1,1.2],'scale':[.96]*3},'fixed':{'rotation':[0,180,0],'scale':[1.05]*3}}
 if k=='crate':return{'thirdperson_righthand':{'rotation':[0,45,0],'translation':[0,2,0],'scale':[.7]*3},'firstperson_righthand':{'rotation':[0,-135,0],'translation':[.8,2.2,.8],'scale':[.82]*3},'fixed':{'rotation':[0,45,0],'scale':[.95]*3}}
 return{'thirdperson_righthand':{'rotation':[0,90,0],'translation':[0,2,0],'scale':[.78]*3},'firstperson_righthand':{'rotation':[0,-90,12],'translation':[1.2,2.6,.8],'scale':[.9]*3},'fixed':{'rotation':[0,180,0],'scale':[1.08]*3}}
A=[];written=set()
def reg(rel,t,icon,k='generic',v=''):
 q=R/'assets/skybit/textures/item'/f'{rel}.png';q.parent.mkdir(parents=True,exist_ok=True);icon.save(q,optimize=True)
 if t not in written:q=R/'assets/skybit/textures/model'/f'{t}.png';q.parent.mkdir(parents=True,exist_ok=True);atlas(t).save(q,optimize=True);written.add(t)
 A.append((rel,t,k,v))
ranks=[('vip','basic'),('knight','rare'),('baron','epic'),('king','legendary'),('emperor','mythic')]
for n,t in ranks:reg(f'vip/{n}_badge',t,badge(t,n),'badge',n)
for t in('basic','rare','epic','legendary','mythic','vote'):
 reg(f'keys/{t}',t,key(t),'key',t);reg(f'fragments/{t}',t,gem(t),'gem',t);reg(f'crates/{t}',t,crate(t),'crate',t)
 if t!='mythic':reg(f'mines/{t}_crystal',t,gem(t),'gem',t)
for rel,t,ic,k,v in[
('currency/skycoin','gold',coin('gold'),'coin','skycoin'),('contracts/daily_contract','basic',card('basic'),'card','daily'),('contracts/weekly_contract','epic',card('epic',True),'card','weekly'),('afk/premium_pass','basic',card('basic'),'card','pass'),('afk/beacon','mythic',core('mythic'),'core','afk'),('enchant/arcane_dust','epic',gem('epic'),'gem','dust'),('enchant/enchant_core','epic',core('epic'),'core','enchant'),('guilds/guild_seal','basic',coin('basic'),'coin','seal'),('bounty/bounty_token','ember',coin('ember'),'coin','bounty'),('treasure/treasure_compass','legendary',ui('legendary','settings'),'generic','compass'),('events/supply_beacon','rare',core('rare'),'core','supply'),('achievements/medal','legendary',badge('legendary','baron'),'badge','medal'),('collections/token','basic',coin('basic'),'coin','collection'),('cozy/hearty_stew','ember',coin('ember'),'generic','food')]:reg(rel,t,ic,k,v)
for n,t in[('relic_shard','epic'),('prosperity','legendary'),('wisdom','rare'),('fortune','vote'),('titan','ember'),('voyager','basic')]:reg(f'relics/{n}',t,gem(t),'gem',n)
for n,t,s in[('miner','basic','settings'),('hunter','ember','booster'),('fisher','rare','links'),('farmer','vote','profile'),('woodcutter','legendary','settings')]:reg(f'professions/{n}',t,ui(t,s),'badge',n)
for n,t in[('bronze','legendary'),('silver','silver'),('gold','gold'),('platinum','rare'),('master','epic')]:reg(f'renown/{n}',t,badge(t,'baron'),'badge',n)
for n,t,s in[('menu','basic','menu'),('profile','rare','profile'),('settings','silver','settings'),('questhub','legendary','booster'),('leaderboard','epic','leaderboard'),('booster','vote','booster'),('serverpass','legendary','profile'),('links','basic','links')]:reg(f'ui/{n}',t,ui(t,s),'generic',n)
for n,t,k in[('skyfang_blade','storm','blade'),('ember_cleaver','ember','cleaver'),('stormcaller_spear','storm','spear'),('void_reaver','void','blade'),('frostbite_bow','rare','bow')]:reg(f'gear/weapons/{n}',t,weapon(t,k),'weapon',k)
reg('gear/tools/titan_pickaxe','gold',weapon('gold','pick'),'weapon','pick')
for s,t in[('stormguard','storm'),('emberforged','ember'),('voidwarden','void')]:
 for p in('helmet','chestplate','leggings','boots'):reg(f'gear/armor/{s}_{p}',t,armor(t,p),'armor',p)
for rel,t,ic,k,v in[('currency/skycoin_pouch','gold',card('gold'),'card','pouch'),('boosters/xp_booster','epic',ui('epic','booster'),'core','xp'),('boosters/money_booster','legendary',coin('legendary'),'coin','money'),('vouchers/fly_voucher','rare',card('rare'),'card','fly'),('vouchers/home_upgrade','basic',card('basic'),'card','home'),('vouchers/repair_token','silver',coin('silver'),'coin','repair'),('cosmetics/trail_core','mythic',core('mythic'),'core','trail'),('cosmetics/nameplate_token','epic',badge('epic','baron'),'badge','nameplate')]:reg(rel,t,ic,k,v)
for rel,t,k,v in A:
 m=R/'assets/skybit/models/item'/f'{rel}_icon.json';m.parent.mkdir(parents=True,exist_ok=True);m.write_text(json.dumps({'parent':'minecraft:item/generated','textures':{'layer0':f'skybit:item/{rel}'}},indent=2))
 dk,e=geo(k,v);m=R/'assets/skybit/models/item'/f'{rel}_3d.json';m.write_text(json.dumps({'textures':{'layer0':f'skybit:model/{t}'},'gui_light':'front','elements':e,'display':disp(dk)},indent=2))
 z={'model':{'type':'minecraft:select','property':'minecraft:display_context','cases':[{'when':['gui','ground'],'model':{'type':'minecraft:model','model':f'skybit:item/{rel}_icon'}}],'fallback':{'type':'minecraft:model','model':f'skybit:item/{rel}_3d'}},'hand_animation_on_swap':False,'oversized_in_gui':False}
 for base in('assets/skybit/items','assets/skybit/items/item'):
  q=R/base/f'{rel}.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(z,indent=2))
for n,t in ranks:
 src=(R/'assets/skybit/items'/f'vip/{n}_badge.json').read_text()
 for x in(f'ranks/{n}',f'rank/{n}'):
  q=R/'assets/skybit/items'/f'{x}.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_text(src)
W=R/'assets/minecraft/textures/gui/sprites/widget';W.mkdir(parents=True,exist_ok=True)
for st,n,col in[('n','button.png',('#071b24','#22cfc8')),('h','button_highlighted.png',('#0b3038','#71fff3')),('d','button_disabled.png',('#10171c','#46535b'))]:
 a=Image.new('RGBA',(200,20));d=ImageDraw.Draw(a);d.rounded_rectangle((1,1,198,18),3,fill=col[0],outline=col[1],width=2);a.save(W/n);(W/(n+'.mcmeta')).write_text(json.dumps({'gui':{'scaling':{'type':'nine_slice','width':200,'height':20,'border':3}}}))
for loc,data in{'sk_sk':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ SPÄŤ DO HRY','menu.disconnect':'§c✖ ODPOJIŤ SA','menu.options':'§e⚙ NASTAVENIA'},'cs_cz':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ ZPĚT DO HRY','menu.disconnect':'§c✖ ODPOJIT SE','menu.options':'§e⚙ NASTAVENÍ'},'en_us':{'menu.game':'§b§l✦ SKYBIT NETWORK ✦','menu.returnToGame':'§a▶ BACK TO SKYBIT','menu.disconnect':'§c✖ LEAVE SKYBIT','menu.options':'§e⚙ SETTINGS'}}.items():q=R/'assets/minecraft/lang'/f'{loc}.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(data,ensure_ascii=False,indent=2))
L=Image.new('RGBA',(256,256),(5,10,16,255));d=ImageDraw.Draw(L);d.polygon([(128,34),(192,71),(184,160),(128,214),(72,160),(64,71)],fill=(6,25,35),outline=(70,234,218),width=5);d.polygon([(128,48),(178,78),(170,151),(128,196),(86,151),(78,78)],fill=(12,54,66),outline=(178,60,232),width=3)
try:
 f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',72);b=d.textbbox((0,0),'SB',font=f);d.text(((256-b[2]+b[0])//2,73),'SB',font=f,fill=(112,248,231))
except:pass
L.save(R/'pack.png');(R/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':PF,'min_format':PF,'max_format':PF,'description':'§b§lSkyBit Network §8• §fPremium Custom Items §d✦ §7(v4.0.0)'}},ensure_ascii=False,indent=2));(R/'SKYBIT-PACK-VERSION.txt').write_text(V+'\n');(R/'SKYBIT-ITEM-MANIFEST.json').write_text(json.dumps({'version':V,'minecraft':'1.21.11','pack_format':PF,'item_count':len(A),'items':[x[0]for x in A]},indent=2));print('SkyBit Premium',V,'items',len(A))
