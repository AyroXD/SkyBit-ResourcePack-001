from pathlib import Path
import hashlib, json, os, shutil, zipfile

ROOT=Path(os.getenv('SKYBIT_BUILD_ROOT','build-v6'))
PACK=ROOT/'SkyBitResourcePack'; DEV=ROOT/'development'
READY=ROOT/'SkyBitResourcePack-v6.0.0-1.21.11-READY.zip'
ALIAS=ROOT/'SkyBitResourcePack.zip'
SHA=ROOT/'SkyBitResourcePack-v6.0.0-1.21.11.sha1.txt'
MANIFEST=ROOT/'release-manifest.json'
PACKAGE=Path('source/SkyBit_3_Key_Package.zip')

KEYS={
 'rare':{
  'id':'skybit:keys/rare','name':'Celestial Azure Key V6 Deluxe',
  'model':'01_Rare_Key_Celestial_Azure/celestial_azure_key_v6_deluxe_minecraft.json',
  'texture':'01_Rare_Key_Celestial_Azure/celestial_azure_key_v6_deluxe.png',
  'display':{
   'thirdperson_righthand':{'rotation':[0,28,-42],'translation':[0,1.6,.5],'scale':[.44,.44,.44]},
   'thirdperson_lefthand':{'rotation':[0,-28,42],'translation':[0,1.6,.5],'scale':[.44,.44,.44]},
   'firstperson_righthand':{'rotation':[0,-22,-34],'translation':[.8,1.8,.5],'scale':[.40,.40,.40]},
   'firstperson_lefthand':{'rotation':[0,22,34],'translation':[.8,1.8,.5],'scale':[.40,.40,.40]},
   'gui':{'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.61,.61,.61]},
   'ground':{'rotation':[0,0,0],'translation':[0,1,0],'scale':[.28,.28,.28]},
   'fixed':{'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.52,.52,.52]}}},
 'epic':{
  'id':'skybit:keys/epic','name':'Cosmic Magenta Key V7 Ultra',
  'model':'02_Epic_Key_Cosmic_Magenta/cosmic_magenta_key_v7_ultra_minecraft.json',
  'texture':'02_Epic_Key_Cosmic_Magenta/cosmic_magenta_key_v7_ultra.png',
  'display':{
   'thirdperson_righthand':{'rotation':[0,28,-42],'translation':[0,1.5,.5],'scale':[.42,.42,.42]},
   'thirdperson_lefthand':{'rotation':[0,-28,42],'translation':[0,1.5,.5],'scale':[.42,.42,.42]},
   'firstperson_righthand':{'rotation':[0,-22,-34],'translation':[.8,1.7,.5],'scale':[.38,.38,.38]},
   'firstperson_lefthand':{'rotation':[0,22,34],'translation':[.8,1.7,.5],'scale':[.38,.38,.38]},
   'gui':{'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.60,.60,.60]},
   'ground':{'rotation':[0,0,0],'translation':[0,1,0],'scale':[.27,.27,.27]},
   'fixed':{'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.50,.50,.50]}}},
 'legendary':{
  'id':'skybit:keys/legendary','name':'Legendary Golden Key V2','source':Path('source/legendary-key-v2'),
  'model':'legendary_golden_key_v2_minecraft.json','texture':'legendary_golden_key_v2.png',
  'display':{
   'thirdperson_righthand':{'rotation':[0,25,-45],'translation':[0,2,.5],'scale':[.52,.52,.52]},
   'thirdperson_lefthand':{'rotation':[0,-25,45],'translation':[0,2,.5],'scale':[.52,.52,.52]},
   'firstperson_righthand':{'rotation':[0,-20,-35],'translation':[1,2.2,.6],'scale':[.52,.52,.52]},
   'firstperson_lefthand':{'rotation':[0,20,35],'translation':[1,2.2,.6],'scale':[.52,.52,.52]},
   'gui':{'rotation':[25,35,-18],'translation':[0,-.2,0],'scale':[1.03,1.03,1.03]},
   'ground':{'rotation':[0,0,0],'translation':[0,1.5,0],'scale':[.38,.38,.38]},
   'fixed':{'rotation':[0,0,-35],'translation':[0,0,0],'scale':[.72,.72,.72]}}},
 'mythic':{
  'id':'skybit:keys/mythic','name':'Astral Empress Key V8',
  'model':'03_Mythic_Key_Astral_Empress/astral_empress_key_v8_minecraft.json',
  'texture':'03_Mythic_Key_Astral_Empress/astral_empress_key_v8.png',
  'display':{
   'thirdperson_righthand':{'rotation':[0,28,-42],'translation':[0,1.4,.5],'scale':[.40,.40,.40]},
   'thirdperson_lefthand':{'rotation':[0,-28,42],'translation':[0,1.4,.5],'scale':[.40,.40,.40]},
   'firstperson_righthand':{'rotation':[0,-22,-34],'translation':[.7,1.6,.5],'scale':[.36,.36,.36]},
   'firstperson_lefthand':{'rotation':[0,22,34],'translation':[.7,1.6,.5],'scale':[.36,.36,.36]},
   'gui':{'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.60,.60,.60]},
   'ground':{'rotation':[0,0,0],'translation':[0,1,0],'scale':[.26,.26,.26]},
   'fixed':{'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.48,.48,.48]}}}}

def writej(p,d):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def fix_uv(m):
 vals=[float(v) for e in m.get('elements',[]) for f in e.get('faces',{}).values() for v in f.get('uv',[])]
 mx=max(vals or [0]); factor=1 if mx<=16.0001 or mx==0 else 16.0/mx
 if factor!=1:
  for e in m.get('elements',[]):
   for f in e.get('faces',{}).values():
    if f.get('uv'): f['uv']=[round(float(v)*factor,4) for v in f['uv']]
 return factor

def itemdef(t):
 return {'model':{'type':'minecraft:select','property':'minecraft:display_context','cases':[{'when':'gui','model':{'type':'minecraft:model','model':f'skybit:item/keys/{t}_icon'}}],'fallback':{'type':'minecraft:model','model':f'skybit:item/keys/{t}_3d'}},'hand_animation_on_swap':False,'oversized_in_gui':False}

def patch_yml(p,ids):
 if not p.exists(): return
 lines=p.read_text(encoding='utf-8').splitlines(); cur=None
 for i,line in enumerate(lines):
  if line.startswith('  - id: '): cur=line.split('"',2)[1] if '"' in line else None
  elif cur in ids and line.strip().startswith('render_mode:'): lines[i]='    render_mode: "2d_gui_3d_held"'
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
 if not PACK.exists(): raise FileNotFoundError(PACK)
 if not PACKAGE.exists(): raise FileNotFoundError(PACKAGE)
 package=zipfile.ZipFile(PACKAGE); applied=[]; ids=set()
 for tier,c in KEYS.items():
  if 'source' in c:
   model=json.loads((c['source']/c['model']).read_text(encoding='utf-8')); tex=(c['source']/c['texture']).read_bytes()
  else:
   model=json.loads(package.read(c['model'])); tex=package.read(c['texture'])
  factor=fix_uv(model); model.setdefault('textures',{})['key']=f'skybit:item/keys/{tier}_3d'; model['textures']['particle']=f'skybit:item/keys/{tier}_3d'; model['display']=c['display']; model['credit']=c['name']+' — SkyBit 3D held/world model'
  md=PACK/f'assets/skybit/models/item/keys/{tier}_3d.json'; td=PACK/f'assets/skybit/textures/item/keys/{tier}_3d.png'
  writej(md,model); td.parent.mkdir(parents=True,exist_ok=True); td.write_bytes(tex)
  idef=itemdef(tier); writej(PACK/f'assets/skybit/items/keys/{tier}.json',idef); writej(PACK/f'assets/skybit/items/item/keys/{tier}.json',idef)
  ids.add(c['id']); applied.append((tier,c['name'],len(model.get('elements',[])),factor))
 package.close()
 reg=DEV/'skybit_item_registry.json'
 if reg.exists():
  d=json.loads(reg.read_text(encoding='utf-8'))
  for x in d.get('items',[]):
   if (x.get('id') or x.get('namespaced_id')) in ids: x['render_mode']='2d_gui_3d_held'
  d['three_d_held_items']=4; d['three_d_held_key_ids']=sorted(ids); writej(reg,d)
 patch_yml(DEV/'skybit-items.yml',ids); patch_yml(DEV/'integration/skybit-items.yml',ids)
 if READY.exists(): READY.unlink()
 with zipfile.ZipFile(READY,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in sorted(PACK.rglob('*')):
   if f.is_file(): z.write(f,f.relative_to(PACK).as_posix())
 shutil.copy2(READY,ALIAS); sha=hashlib.sha1(READY.read_bytes()).hexdigest(); SHA.write_text(sha+'\n')
 man=json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}; man['sha1']=sha; man['three_d_held_items']=4; man['three_d_held_keys']={t:{'name':c['name'],'render_mode':'2d_gui_3d_held','model':f'skybit:item/keys/{t}_3d'} for t,c in KEYS.items()}; writej(MANIFEST,man)
 rep=DEV/'VALIDATION_REPORT.md'
 if rep.exists():
  s=rep.read_text(encoding='utf-8').rstrip()+'\n\n## Premium 3D held keys\n'
  for t,n,e,f in applied: s+=f'- {t.title()} — **{n}**: 2D GUI + 3D held/world, {e} elements, UV factor `{f:g}`.\n'
  rep.write_text(s+f'- SHA1: `{sha}`\n',encoding='utf-8')
 for x in applied: print(x)
 print('SHA1:',sha)

if __name__=='__main__': main()
