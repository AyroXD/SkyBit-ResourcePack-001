from pathlib import Path
import json
ready=Path('build/SkyBit-ResourcePack')
texroot=ready/'assets/skybit/textures/item'

def face(tile):
    col=tile%4; row=tile//4; u0=col*4; v0=row*4; uv=[u0,v0,u0+4,v0+4]
    return {k:{'uv':uv,'texture':'#layer0'} for k in ['north','south','east','west','up','down']}

def cube(a,b,c,d,e,f,tile): return {'from':[a,b,c],'to':[d,e,f],'faces':face(tile)}

def display(kind):
    if kind=='weapon': return {'thirdperson_righthand':{'rotation':[0,92,0],'translation':[0,2.25,1],'scale':[0.82,0.82,0.82]},'thirdperson_lefthand':{'rotation':[0,88,0],'translation':[0,2.25,1],'scale':[0.82,0.82,0.82]},'firstperson_righthand':{'rotation':[0,-90,24],'translation':[1.35,3.1,1.2],'scale':[0.96,0.96,0.96]},'firstperson_lefthand':{'rotation':[0,90,-24],'translation':[1.35,3.1,1.2],'scale':[0.96,0.96,0.96]},'gui':{'rotation':[22,225,0],'translation':[0,-1,0],'scale':[1,1,1]},'ground':{'translation':[0,3,0],'scale':[0.72]*3},'fixed':{'rotation':[0,180,0],'scale':[1.1]*3}}
    if kind=='crate': return {'thirdperson_righthand':{'rotation':[0,45,0],'translation':[0,2,0],'scale':[0.7]*3},'thirdperson_lefthand':{'rotation':[0,45,0],'translation':[0,2,0],'scale':[0.7]*3},'firstperson_righthand':{'rotation':[0,-135,0],'translation':[0.8,2.2,0.8],'scale':[0.82]*3},'firstperson_lefthand':{'rotation':[0,135,0],'translation':[0.8,2.2,0.8],'scale':[0.82]*3},'gui':{'rotation':[23,225,0],'translation':[0,-1,0],'scale':[0.94]*3},'ground':{'translation':[0,3,0],'scale':[0.65]*3},'fixed':{'rotation':[0,45,0],'scale':[0.9]*3}}
    return {'thirdperson_righthand':{'rotation':[0,90,0],'translation':[0,2,0],'scale':[0.78]*3},'thirdperson_lefthand':{'rotation':[0,90,0],'translation':[0,2,0],'scale':[0.78]*3},'firstperson_righthand':{'rotation':[0,-90,12],'translation':[1.2,2.6,0.8],'scale':[0.9]*3},'firstperson_lefthand':{'rotation':[0,90,-12],'translation':[1.2,2.6,0.8],'scale':[0.9]*3},'gui':{'rotation':[28,225,0],'translation':[0,0,0],'scale':[1.08]*3},'ground':{'translation':[0,2.5,0],'scale':[0.68]*3},'fixed':{'rotation':[0,180,0],'scale':[1.08]*3}}

def model(tex,kind,els): return {'textures':{'layer0':tex},'gui_light':'front','elements':els,'display':display(kind)}

def custom(path,tex):
    if path=='crates/mythic': return model(tex,'crate',[cube(2.8,1,2.8,13.2,8.2,13.2,0),cube(2,8.2,2,14,12.6,14,1),cube(2.5,3.1,2,13.5,4.8,3.4,6),cube(6.7,4.3,1.4,9.3,8.7,3.9,3),cube(0.8,7.8,6.2,3,12.7,9.8,7),cube(13,7.8,6.2,15.2,12.7,9.8,7),cube(5.5,12.1,6.2,7.1,15.7,9.8,6),cube(8.9,12.1,6.2,10.5,15.7,9.8,6)])
    if path=='crates/legendary': return model(tex,'crate',[cube(3,1,3,13,8,13,0),cube(2.1,8,2.1,13.9,12.4,13.9,1),cube(2.8,3.4,2.2,13.2,4.8,3.4,5),cube(7,4.6,1.5,9,8.4,3.8,3),cube(4.2,12.2,6.8,6,15.2,9.2,3),cube(7.1,12.4,6.7,8.9,15.8,9.3,3),cube(10,12.2,6.8,11.8,15.2,9.2,3)])
    if path.startswith('crates/'): return model(tex,'crate',[cube(3,1,3,13,8,13,0),cube(2.3,8,2.3,13.7,12.6,13.7,1),cube(3.5,4,2.4,12.5,5,3.3,5),cube(7,4.8,1.8,9,8.2,3.8,3),cube(3.5,9.2,12.7,12.5,10.2,13.6,5)])
    if path.startswith('keys/'): return model(tex,'small',[cube(7,1,7,9.2,10.6,9,5),cube(4.8,9.6,7,11.4,12,9,1),cube(4.8,6.4,7,7,9.6,9,1),cube(9.2,6.4,7,11.4,9.6,9,2),cube(7,0,7,10.4,2.2,9,3),cube(9.2,2.2,7,11.6,4.4,9,3)])
    if path.startswith('fragments/') or path.startswith('mines/') or 'crystal' in path: return model(tex,'small',[cube(7,2,7,9,11.8,9,1),cube(5.7,5,7,7,9,9,0),cube(9,6.2,7,10.3,10.2,9,2),cube(7.2,11.8,7.2,8.8,15.1,8.8,6)])
    if path=='afk/beacon': return model(tex,'small',[cube(5,2,5,11,4,11,0),cube(6.2,4,6.2,9.8,8,9.8,1),cube(7,8,7,9,14,9,6),cube(5.2,10.5,7.3,10.8,11.7,8.7,3)])
    if path.startswith('gear/armor/'):
        if path.endswith('helmet'): els=[cube(4.8,5,5.2,11.2,11.4,10.8,1),cube(5.4,4.1,5.7,10.6,6,10.3,0),cube(4.2,7,6,5.2,10.5,10,3),cube(10.8,7,6,11.8,10.5,10,3)]
        elif path.endswith('chestplate'): els=[cube(5.2,4,6.3,10.8,12,9.7,1),cube(2.8,5,6.5,5.2,9.8,9.5,2),cube(10.8,5,6.5,13.2,9.8,9.5,2),cube(6,11.7,6.5,10,14.2,9.5,3)]
        elif path.endswith('leggings'): els=[cube(4.8,9,6.5,11.2,12,9.5,1),cube(5,3,6.6,7.5,9.3,9.4,1),cube(8.5,3,6.6,11,9.3,9.4,1),cube(4.4,11.8,6.4,11.6,13.5,9.6,3)]
        else: els=[cube(4.5,3,6.4,7.5,7.5,9.6,1),cube(8.5,3,6.4,11.5,7.5,9.6,1),cube(4,2,5.8,7.8,4,10.2,3),cube(8.2,2,5.8,12,4,10.2,3)]
        return model(tex,'small',els)
    if 'skyfang_blade' in path or 'void_reaver' in path: return model(tex,'weapon',[cube(6.4,0,6.4,9.6,2,9.6,4),cube(7,2,7,9,6.4,9,4),cube(4.6,6.1,6.25,11.4,7.4,9.75,3),cube(7.1,7.4,7.1,8.9,14.6,8.9,1),cube(7.35,14.6,7.35,8.65,16,8.65,2)])
    if 'ember_cleaver' in path: return model(tex,'weapon',[cube(6.7,0,6.7,9.3,2,9.3,4),cube(7.1,2,7.1,8.9,12.8,8.9,4),cube(6.2,9.4,6,11.8,14.6,10,1),cube(3.6,8.3,6,6.2,14.1,10,2),cube(10.9,11.4,6.4,13.2,15.2,9.6,3)])
    if 'stormcaller_spear' in path: return model(tex,'weapon',[cube(7,0,7,9,2,9,4),cube(7.25,2,7.25,8.75,13.2,8.75,4),cube(6.1,12.5,6.8,9.9,13.6,9.2,3),cube(6.9,13.2,6.9,9.1,15.2,9.1,1),cube(7.2,15.2,7.2,8.8,16,8.8,2)])
    if 'titan_pickaxe' in path: return model(tex,'weapon',[cube(6.8,0,6.8,9.2,2,9.2,4),cube(7.1,2,7.1,8.9,12.7,8.9,4),cube(3.1,11,6.3,12.9,13.6,9.7,1),cube(2,12.3,6.1,4,15,9.9,2),cube(12,9.9,6.2,14.3,12.9,9.8,3)])
    if 'frostbite_bow' in path: return model(tex,'weapon',[cube(4.8,2,7.2,6.2,6,8.8,1),cube(5.6,6,7.2,6.8,10,8.8,1),cube(4.8,10,7.2,6.2,14,8.8,2),cube(8,5.8,7,9.6,10.2,9,4),cube(10.8,2,7.2,12.2,6,8.8,1),cube(10.2,6,7.2,11.4,10,8.8,1),cube(10.8,10,7.2,12.2,14,8.8,2),cube(8,2,7.75,8.35,14,8.25,6)])
    if 'skycoin' in path or 'seal' in path or 'token' in path or path.startswith('renown/'): return model(tex,'small',[cube(4,4,7,12,12,9,1),cube(5.2,5.2,6.4,10.8,10.8,9.6,3),cube(6.5,6.5,5.8,9.5,9.5,10.2,6)])
    if 'daily_contract' in path or 'weekly_contract' in path: return model(tex,'small',[cube(4,2,7,6,14,9,5),cube(6,3,7.2,10,13,8.8,8),cube(10,2,7,12,14,9,5),cube(7.2,1,6.6,9.8,3,9.4,3)])
    if 'premium_pass' in path: return model(tex,'small',[cube(3.2,5,7,12.8,11,9,1),cube(5,10.6,7,6.8,12.4,9,3),cube(9.2,10.6,7,11,12.4,9,3),cube(7,6.2,6.2,9,8.2,9.8,6)])
    if '_badge' in path: return model(tex,'small',[cube(5,4,6.8,11,10,9.2,1),cube(6.2,10,7,7.8,14.6,9,3),cube(8.2,10,7,9.8,14.6,9,3),cube(6,5,6.2,10,9,9.8,6)])
    return {'parent':'minecraft:item/generated','textures':{'layer0':tex}}

for texfile in (ready/'assets/skybit/textures/item').rglob('*.png'):
    path=texfile.relative_to(ready/'assets/skybit/textures/item').with_suffix('').as_posix()
    m=custom(path,'skybit:item/'+path)
    mp=ready/'assets/skybit/models/item'/f'{path}.json'; mp.parent.mkdir(parents=True,exist_ok=True); mp.write_text(json.dumps(m,indent=2),encoding='utf-8')
    ip=ready/'assets/skybit/items'/f'{path}.json'; ip.parent.mkdir(parents=True,exist_ok=True); ip.write_text(json.dumps({'model':{'type':'minecraft:model','model':'skybit:item/'+path}},indent=2),encoding='utf-8')
print('models',len(list((ready/'assets/skybit/models/item').rglob('*.json'))))