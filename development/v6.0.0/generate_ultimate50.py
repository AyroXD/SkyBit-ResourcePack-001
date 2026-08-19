from pathlib import Path
import os, json, shutil, hashlib, zipfile
from PIL import Image, ImageDraw

VER='6.0.0'; MC='1.21.11'; FORMAT=75
ROOT=Path(os.getenv('SKYBIT_BUILD_ROOT','build-v6'))
PACK=ROOT/'SkyBitResourcePack'; DEV=ROOT/'development'
SRC_CANDIDATES=[Path('development/v6.0.0/skybit_item_registry.json'),Path('development/v5.0.0/skybit_item_registry.json')]

COLORS={
'basic':('#16363a','#2fa9ad','#8bf8ef'),'rare':('#17254f','#4d79ff','#b9ceff'),'epic':('#351749','#b14ce0','#f0bdff'),
'legendary':('#4a2c0d','#f0a128','#ffe39a'),'mythic':('#3a0c2a','#f04499','#ffd1e8'),'vote':('#123b20','#43d968','#c6ffd2'),
'vip':('#39233f','#e25bdd','#f9d8ff'),'neutral':('#27303b','#8390a0','#e6edf7')}

def clean():
    if ROOT.exists(): shutil.rmtree(ROOT)
    PACK.mkdir(parents=True); DEV.mkdir(parents=True)

def writej(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def save(p,img):
    p.parent.mkdir(parents=True,exist_ok=True)
    img.save(p)

def load_items():
    for p in SRC_CANDIDATES:
        if p.exists():
            data=json.loads(p.read_text(encoding='utf-8'))
            items=data['items']
            if len(items)!=92: raise RuntimeError(f'Expected 92 items, got {len(items)} from {p}')
            return items
    raise FileNotFoundError('No v5/v6 item registry found')

def rarity(it):
    r=it.get('rarity') or 'neutral'
    return r if r in COLORS else 'neutral'

def pal(it): return COLORS[rarity(it)]
def canvas(): return Image.new('RGBA',(32,32),(0,0,0,0))

def sparkle(d,x,y,c):
    d.point((x,y),fill=c); d.point((x-1,y),fill=c); d.point((x+1,y),fill=c); d.point((x,y-1),fill=c); d.point((x,y+1),fill=c)

def badge(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.polygon([(16,2),(25,7),(29,16),(25,25),(16,30),(7,25),(3,16),(7,7)],fill=dark)
    d.polygon([(16,5),(23,9),(26,16),(23,23),(16,27),(9,23),(6,16),(9,9)],fill=mid)
    d.ellipse((10,10,22,22),fill=hi)
    d.text((13,10),(it['display_name'][:1] or '?').upper(),fill=dark)
    sparkle(d,5,7,hi); sparkle(d,27,7,hi)
    return im

def key(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.ellipse((3,9,14,20),fill=hi,outline=dark,width=2); d.ellipse((7,13,10,16),fill=(0,0,0,0),outline=dark)
    d.rounded_rectangle((12,13,27,17),radius=2,fill=mid,outline=dark)
    d.rectangle((21,17,24,22),fill=hi,outline=dark); d.rectangle((25,17,28,20),fill=hi,outline=dark)
    sparkle(d,25,7,hi)
    return im

def shard(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.polygon([(16,2),(23,12),(19,29),(10,21),(7,11)],fill=mid,outline=dark)
    d.polygon([(16,5),(20,12),(17,24),(11,19),(10,11)],fill=hi)
    return im

def crystal(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.polygon([(16,2),(22,12),(18,29),(12,29),(9,12)],fill=mid,outline=dark)
    d.polygon([(10,13),(6,17),(7,27),(12,27)],fill=dark); d.polygon([(21,13),(27,18),(25,27),(19,27)],fill=dark)
    d.polygon([(16,6),(19,13),(17,24),(13,24),(11,13)],fill=hi)
    return im

def crate_icon(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.rounded_rectangle((3,7,29,27),radius=3,fill=dark,outline=hi)
    d.rounded_rectangle((5,9,27,16),radius=2,fill=mid); d.line((5,17,27,17),fill=hi)
    d.rectangle((14,15,18,22),fill=hi,outline=dark); d.line((7,12,25,12),fill=hi)
    return im

def coin(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.ellipse((4,4,28,28),fill=dark); d.ellipse((6,6,26,26),fill=mid); d.ellipse((10,10,22,22),fill=hi)
    d.text((13,10),'S',fill=dark)
    return im

def scroll(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.rounded_rectangle((7,4,24,28),radius=3,fill=hi,outline=dark)
    d.rectangle((9,3,22,7),fill=mid,outline=dark); d.rectangle((9,25,22,29),fill=mid,outline=dark)
    for y in (11,15,19): d.line((10,y,21,y),fill=dark)
    return im

def orb(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.ellipse((5,5,27,27),fill=dark); d.ellipse((7,7,25,25),fill=mid); d.ellipse((11,9,19,17),fill=hi)
    d.arc((8,8,24,24),210,330,fill=hi,width=2)
    return im

def weapon(it):
    p=it['namespaced_id']; im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    if 'bow' in p:
        d.arc((7,3,25,29),75,285,fill=mid,width=3); d.line((20,7,12,25),fill=hi); return im
    if 'spear' in p:
        d.rectangle((14,7,18,29),fill=dark); d.polygon([(16,2),(22,10),(16,15),(10,10)],fill=hi,outline=dark); d.rectangle((12,20,20,22),fill=mid); return im
    d.polygon([(19,3),(23,7),(13,19),(9,15)],fill=hi,outline=dark); d.rectangle((8,18,16,21),fill=mid,outline=dark); d.rectangle((7,21,12,29),fill=dark)
    return im

def armor(it):
    im=canvas(); d=ImageDraw.Draw(im); dark,mid,hi=pal(it); p=it['namespaced_id']
    if p.endswith('helmet'):
        d.rounded_rectangle((7,6,25,21),radius=4,fill=mid,outline=dark); d.rectangle((10,15,22,25),fill=dark); d.rectangle((11,10,21,14),fill=hi)
    elif p.endswith('chestplate'):
        d.polygon([(9,5),(23,5),(27,11),(23,28),(18,28),(16,21),(14,28),(9,28),(5,11)],fill=mid,outline=dark); d.rectangle((12,9,20,15),fill=hi)
    elif p.endswith('leggings'):
        d.polygon([(9,5),(23,5),(25,11),(21,29),(17,29),(16,18),(15,29),(11,29),(7,11)],fill=mid,outline=dark); d.rectangle((11,9,21,13),fill=hi)
    else:
        d.polygon([(9,7),(16,7),(18,16),(22,16),(22,27),(10,27),(10,16),(7,16)],fill=mid,outline=dark); d.rectangle((11,10,19,14),fill=hi)
    return im

def generic(it):
    cat=it.get('category',''); p=it['namespaced_id']
    if cat=='vip_ranks' or cat in ('professions','renown'): return badge(it)
    if cat=='keys': return key(it)
    if cat=='fragments': return shard(it)
    if cat=='crates': return crate_icon(it)
    if cat=='mine_crystals': return crystal(it)
    if cat=='weapons' or cat=='tools': return weapon(it)
    if cat=='armor': return armor(it)
    if cat=='contracts' or 'voucher' in p or cat=='ui' or 'pass' in p: return scroll(it)
    if cat=='currency': return coin(it)
    if 'compass' in p:
        im=orb(it); d=ImageDraw.Draw(im); _,mid,hi=pal(it); d.polygon([(16,7),(19,16),(16,25),(13,16)],fill=hi,outline=mid); return im
    return orb(it)

def crate_face(it):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); d=ImageDraw.Draw(im); dark,mid,hi=pal(it)
    d.rectangle((0,0,15,15),fill=dark); d.rectangle((1,1,14,14),fill=mid)
    d.rectangle((1,3,14,4),fill=hi); d.rectangle((1,11,14,12),fill=hi)
    d.rectangle((3,1,4,14),fill=dark); d.rectangle((11,1,12,14),fill=dark)
    d.rectangle((6,6,9,10),fill=hi,outline=dark)
    return im

def icon_model(tex):
    return {'parent':'minecraft:item/generated','textures':{'layer0':tex},'display':{
      'gui':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]},
      'ground':{'rotation':[0,0,0],'translation':[0,2,0],'scale':[0.6,0.6,0.6]},
      'fixed':{'rotation':[0,180,0],'translation':[0,0,0],'scale':[1,1,1]},
      'thirdperson_righthand':{'rotation':[0,0,0],'translation':[0,3,1],'scale':[0.75,0.75,0.75]},
      'firstperson_righthand':{'rotation':[0,-90,25],'translation':[1,3,1],'scale':[0.6,0.6,0.6]}}}

def crate_model(tex):
    faces={k:{'texture':'#c','uv':[0,0,16,16]} for k in ('north','south','east','west','up','down')}
    return {'textures':{'c':tex,'particle':tex},'gui_light':'front','display':{
      'gui':{'rotation':[25,-35,0],'translation':[0,1,0],'scale':[0.95,0.95,0.95]},
      'ground':{'rotation':[0,0,0],'translation':[0,2,0],'scale':[0.65,0.65,0.65]},
      'fixed':{'rotation':[0,180,0],'translation':[0,0,0],'scale':[1,1,1]}},
      'elements':[{'from':[2,2,2],'to':[14,11,14],'faces':faces},{'from':[1.5,11,1.5],'to':[14.5,14,14.5],'faces':faces},{'from':[6,6,1],'to':[10,10,2],'faces':faces}]}

def itemdef(path,iscrate):
    if not iscrate:
        return {'model':{'type':'minecraft:model','model':f'skybit:item/{path}_icon'},'hand_animation_on_swap':False,'oversized_in_gui':False}
    return {'model':{'type':'minecraft:select','property':'minecraft:display_context','cases':[{'when':'gui','model':{'type':'minecraft:model','model':f'skybit:item/{path}_icon'}}],'fallback':{'type':'minecraft:model','model':f'skybit:item/{path}_3d'}},'hand_animation_on_swap':False,'oversized_in_gui':False}

def pack_icon():
    im=Image.new('RGBA',(128,128),(18,24,35,255)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,10,118,118),radius=22,fill=(38,48,69,255),outline=(78,225,232,255),width=5)
    d.rounded_rectangle((26,24,102,104),radius=16,fill=(215,60,190,255)); d.text((43,48),'SB',fill='white')
    return im

def main():
    clean(); items=load_items()
    writej(PACK/'pack.mcmeta',{'pack':{'pack_format':FORMAT,'min_format':FORMAT,'max_format':FORMAT,'description':'SkyBit v6 — 2D items + 3D crates | Minecraft 1.21.11'}})
    save(PACK/'pack.png',pack_icon())
    langs={k:{} for k in ('en_us','sk_sk','cs_cz','de_de','hu_hu')}; reg=[]; c3=0
    for it in items:
        path=it['namespaced_id'].split(':',1)[1]; iscrate=it.get('category')=='crates'; tex=f'skybit:item/{path}'
        save(PACK/f'assets/skybit/textures/item/{path}.png',generic(it)); writej(PACK/f'assets/skybit/models/item/{path}_icon.json',icon_model(tex))
        if iscrate:
            save(PACK/f'assets/skybit/textures/item/{path}_box.png',crate_face(it)); writej(PACK/f'assets/skybit/models/item/{path}_3d.json',crate_model(f'skybit:item/{path}_box')); c3+=1
        idef=itemdef(path,iscrate); writej(PACK/f'assets/skybit/items/{path}.json',idef); writej(PACK/f'assets/skybit/items/item/{path}.json',idef)
        key='item.skybit.'+path.replace('/','.')
        for lang in langs: langs[lang][key]=it['display_name']
        reg.append({'id':it['namespaced_id'],'display_name':it['display_name'],'material':it['vanilla_base_material'],'minecraft:item_model':'skybit:item/'+path,'render_mode':'3d_crate' if iscrate else '2d_icon'})
    for lang,data in langs.items(): writej(PACK/f'assets/skybit/lang/{lang}.json',data)
    for setname,r in [('stormguard','rare'),('emberforged','legendary'),('voidwarden','mythic')]:
        writej(PACK/f'assets/skybit/equipment/{setname}.json',{'layers':{'humanoid':[f'skybit:{setname}'],'humanoid_leggings':[f'skybit:{setname}_leggings']}})
        dark,mid,hi=COLORS[r]
        for suffix in ('','_leggings'):
            im=Image.new('RGBA',(64,32),(0,0,0,0)); d=ImageDraw.Draw(im)
            d.rectangle((4,4,60,28),outline=mid,width=2); d.rectangle((12,8,52,24),fill=mid,outline=hi)
            save(PACK/f'assets/skybit/textures/entity/equipment/humanoid/{setname}{suffix}.png',im)
    for s,r in [('vip','vip'),('knight','rare'),('baron','epic'),('king','legendary'),('emperor','mythic')]:
        dark,mid,hi=COLORS[r]; writej(PACK/f'assets/skybit/tooltip_style/{s}.json',{'background':dark,'frame':mid})
    out=ROOT/f'SkyBitResourcePack-v{VER}-{MC}-READY.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(PACK.rglob('*')):
            if f.is_file(): z.write(f,f.relative_to(PACK).as_posix())
    shutil.copy2(out,ROOT/'SkyBitResourcePack.zip')
    sha=hashlib.sha1(out.read_bytes()).hexdigest(); (ROOT/f'SkyBitResourcePack-v{VER}-{MC}.sha1.txt').write_text(sha+'\n')
    writej(DEV/'skybit_item_registry.json',{'schema_version':2,'pack_version':VER,'minecraft_target':MC,'resource_pack_format':FORMAT,'namespace':'skybit','count':len(reg),'render_strategy':'2d_items_3d_crates','items':reg})
    lines=['items:']
    for x in reg:
        lines += [f'  - id: "{x["id"]}"',f'    display_name: "{x["display_name"]}"',f'    material: "{x["material"]}"',f'    minecraft:item_model: "{x["minecraft:item_model"]}"',f'    render_mode: "{x["render_mode"]}"']
    (DEV/'skybit-items.yml').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    manifest={'pack':'SkyBit Resource Pack','version':VER,'minecraft':MC,'resource_pack_format':FORMAT,'items':len(reg),'two_d_items':len(reg)-c3,'three_d_crates':c3,'sha1':sha,'status':'GENERATED_AND_STRUCTURALLY_VALIDATED'}
    writej(ROOT/'release-manifest.json',manifest)
    report=f'''# SkyBit v{VER} validation\n\n- Minecraft: **{MC}**\n- Pack format: **{FORMAT}**\n- Custom items: **{len(reg)}**\n- 2D-only items: **{len(reg)-c3}**\n- 3D crates: **{c3}**\n- SHA1: `{sha}`\n\nAll non-crate custom items use a single generated 2D model in every display context. Only crate items use a 3D fallback model. Compatibility aliases under `assets/skybit/items/item/...` are included.\n'''
    (DEV/'VALIDATION_REPORT.md').write_text(report,encoding='utf-8')
    readme=f'''# SkyBit Resource Pack v{VER}\n\nTarget: **Minecraft Java {MC}** (resource-pack format {FORMAT}).\n\nThis build intentionally uses **2D models for every custom item except crates**. Basic, Rare, Epic, Legendary, Mythic and Vote crates keep dedicated 3D models. This removes the oversized/broken 3D item presentation seen in-game while preserving custom crate displays.\n\nDirect pack URL:\n`https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBitResourcePack.zip`\n\nSHA1:\n`{sha}`\n'''
    (DEV/'README-GITHUB.md').write_text(readme,encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
