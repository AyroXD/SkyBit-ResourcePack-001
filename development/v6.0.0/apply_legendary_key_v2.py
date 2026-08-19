from pathlib import Path
import hashlib, json, os, shutil, zipfile

ROOT = Path(os.getenv('SKYBIT_BUILD_ROOT', 'build-v6'))
PACK = ROOT / 'SkyBitResourcePack'
DEV = ROOT / 'development'
READY = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11-READY.zip'
ALIAS = ROOT / 'SkyBitResourcePack.zip'
SHA = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11.sha1.txt'
MANIFEST = ROOT / 'release-manifest.json'
PACKAGE = Path('source/SkyBit_3_Key_Runtime_Sources.zip')

KEYS = {
    'rare': {
        'id': 'skybit:keys/rare', 'name': 'Celestial Azure Key V6 Deluxe',
        'model': 'rare/celestial_azure_key_v6_deluxe_minecraft.json',
        'texture': 'rare/celestial_azure_key_v6_deluxe.png',
        'display': {
            'thirdperson_righthand': {'rotation':[0,28,-42],'translation':[0,1.6,.5],'scale':[.44,.44,.44]},
            'thirdperson_lefthand': {'rotation':[0,-28,42],'translation':[0,1.6,.5],'scale':[.44,.44,.44]},
            'firstperson_righthand': {'rotation':[0,-22,-34],'translation':[.8,1.8,.5],'scale':[.40,.40,.40]},
            'firstperson_lefthand': {'rotation':[0,22,34],'translation':[.8,1.8,.5],'scale':[.40,.40,.40]},
            'gui': {'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.61,.61,.61]},
            'ground': {'rotation':[0,0,0],'translation':[0,1,0],'scale':[.28,.28,.28]},
            'fixed': {'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.52,.52,.52]}
        }
    },
    'epic': {
        'id': 'skybit:keys/epic', 'name': 'Cosmic Magenta Key V7 Ultra',
        'model': 'epic/cosmic_magenta_key_v7_ultra_minecraft.json',
        'texture': 'epic/cosmic_magenta_key_v7_ultra.png',
        'display': {
            'thirdperson_righthand': {'rotation':[0,28,-42],'translation':[0,1.5,.5],'scale':[.42,.42,.42]},
            'thirdperson_lefthand': {'rotation':[0,-28,42],'translation':[0,1.5,.5],'scale':[.42,.42,.42]},
            'firstperson_righthand': {'rotation':[0,-22,-34],'translation':[.8,1.7,.5],'scale':[.38,.38,.38]},
            'firstperson_lefthand': {'rotation':[0,22,34],'translation':[.8,1.7,.5],'scale':[.38,.38,.38]},
            'gui': {'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.60,.60,.60]},
            'ground': {'rotation':[0,0,0],'translation':[0,1,0],'scale':[.27,.27,.27]},
            'fixed': {'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.50,.50,.50]}
        }
    },
    'legendary': {
        'id': 'skybit:keys/legendary', 'name': 'Legendary Golden Key V2',
        'source': Path('source/legendary-key-v2'),
        'model': 'legendary_golden_key_v2_minecraft.json', 'texture': 'legendary_golden_key_v2.png',
        'display': {
            'thirdperson_righthand': {'rotation':[0,25,-45],'translation':[0,2,.5],'scale':[.52,.52,.52]},
            'thirdperson_lefthand': {'rotation':[0,-25,45],'translation':[0,2,.5],'scale':[.52,.52,.52]},
            'firstperson_righthand': {'rotation':[0,-20,-35],'translation':[1,2.2,.6],'scale':[.52,.52,.52]},
            'firstperson_lefthand': {'rotation':[0,20,35],'translation':[1,2.2,.6],'scale':[.52,.52,.52]},
            'gui': {'rotation':[25,35,-18],'translation':[0,-.2,0],'scale':[1.03,1.03,1.03]},
            'ground': {'rotation':[0,0,0],'translation':[0,1.5,0],'scale':[.38,.38,.38]},
            'fixed': {'rotation':[0,0,-35],'translation':[0,0,0],'scale':[.72,.72,.72]}
        }
    },
    'mythic': {
        'id': 'skybit:keys/mythic', 'name': 'Astral Empress Key V8',
        'model': 'mythic/astral_empress_key_v8_minecraft.json',
        'texture': 'mythic/astral_empress_key_v8.png',
        'display': {
            'thirdperson_righthand': {'rotation':[0,28,-42],'translation':[0,1.4,.5],'scale':[.40,.40,.40]},
            'thirdperson_lefthand': {'rotation':[0,-28,42],'translation':[0,1.4,.5],'scale':[.40,.40,.40]},
            'firstperson_righthand': {'rotation':[0,-22,-34],'translation':[.7,1.6,.5],'scale':[.36,.36,.36]},
            'firstperson_lefthand': {'rotation':[0,22,34],'translation':[.7,1.6,.5],'scale':[.36,.36,.36]},
            'gui': {'rotation':[18,30,-28],'translation':[0,-1.5,0],'scale':[.60,.60,.60]},
            'ground': {'rotation':[0,0,0],'translation':[0,1,0],'scale':[.26,.26,.26]},
            'fixed': {'rotation':[0,0,-34],'translation':[0,-.5,0],'scale':[.48,.48,.48]}
        }
    }
}


def writej(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def fix_uv(model):
    values = [float(v) for e in model.get('elements',[]) for f in e.get('faces',{}).values() for v in f.get('uv',[])]
    maximum = max(values or [0])
    factor = 1.0 if maximum <= 16.0001 or maximum == 0 else 16.0 / maximum
    if factor != 1.0:
        for e in model.get('elements',[]):
            for f in e.get('faces',{}).values():
                if f.get('uv'):
                    f['uv'] = [round(float(v) * factor, 4) for v in f['uv']]
    return factor


def itemdef(tier):
    return {
        'model': {
            'type':'minecraft:select', 'property':'minecraft:display_context',
            'cases':[{'when':'gui','model':{'type':'minecraft:model','model':f'skybit:item/keys/{tier}_icon'}}],
            'fallback':{'type':'minecraft:model','model':f'skybit:item/keys/{tier}_3d'}
        },
        'hand_animation_on_swap':False, 'oversized_in_gui':False
    }


def patch_yml(path, ids):
    if not path.exists(): return
    lines = path.read_text(encoding='utf-8').splitlines(); current = None
    for i, line in enumerate(lines):
        if line.startswith('  - id: '):
            current = line.split('"',2)[1] if '"' in line else None
        elif current in ids and line.strip().startswith('render_mode:'):
            lines[i] = '    render_mode: "2d_gui_3d_held"'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify_package():
    if not PACKAGE.exists(): raise FileNotFoundError(PACKAGE)
    expected = {KEYS[t][k] for t in ('rare','epic','mythic') for k in ('model','texture')}
    try:
        with zipfile.ZipFile(PACKAGE) as z:
            bad = z.testzip()
            if bad: raise RuntimeError(f'Corrupt runtime key package entry: {bad}')
            missing = sorted(expected - set(z.namelist()))
            if missing: raise RuntimeError('Runtime key package missing: ' + ', '.join(missing))
    except zipfile.BadZipFile as exc:
        raise RuntimeError('Runtime premium key package is not a valid ZIP') from exc


def main():
    if not PACK.exists(): raise FileNotFoundError(PACK)
    verify_package()
    applied=[]; ids=set()
    with zipfile.ZipFile(PACKAGE) as package:
        for tier, cfg in KEYS.items():
            if 'source' in cfg:
                model=json.loads((cfg['source']/cfg['model']).read_text(encoding='utf-8'))
                texture=(cfg['source']/cfg['texture']).read_bytes()
            else:
                model=json.loads(package.read(cfg['model']).decode('utf-8'))
                texture=package.read(cfg['texture'])
            factor=fix_uv(model)
            model.setdefault('textures',{})['key']=f'skybit:item/keys/{tier}_3d'
            model['textures']['particle']=f'skybit:item/keys/{tier}_3d'
            model['display']=cfg['display']
            model['credit']=cfg['name'] + ' — SkyBit 3D held/world model'
            writej(PACK/f'assets/skybit/models/item/keys/{tier}_3d.json', model)
            tex=PACK/f'assets/skybit/textures/item/keys/{tier}_3d.png'; tex.parent.mkdir(parents=True,exist_ok=True); tex.write_bytes(texture)
            definition=itemdef(tier)
            writej(PACK/f'assets/skybit/items/keys/{tier}.json',definition)
            writej(PACK/f'assets/skybit/items/item/keys/{tier}.json',definition)
            ids.add(cfg['id']); applied.append((tier,cfg['name'],len(model.get('elements',[])),factor))

    registry=DEV/'skybit_item_registry.json'
    if registry.exists():
        data=json.loads(registry.read_text(encoding='utf-8'))
        for item in data.get('items',[]):
            if (item.get('id') or item.get('namespaced_id')) in ids: item['render_mode']='2d_gui_3d_held'
        data['three_d_held_items']=4; data['three_d_held_key_ids']=sorted(ids); writej(registry,data)
    patch_yml(DEV/'skybit-items.yml',ids); patch_yml(DEV/'integration/skybit-items.yml',ids)

    if READY.exists(): READY.unlink()
    with zipfile.ZipFile(READY,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(PACK.rglob('*')):
            if f.is_file(): z.write(f,f.relative_to(PACK).as_posix())
    shutil.copy2(READY,ALIAS)
    sha1=hashlib.sha1(READY.read_bytes()).hexdigest(); SHA.write_text(sha1+'\n',encoding='utf-8')
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    manifest['sha1']=sha1; manifest['three_d_held_items']=4
    manifest['three_d_held_keys']={tier:{'name':cfg['name'],'render_mode':'2d_gui_3d_held','model':f'skybit:item/keys/{tier}_3d'} for tier,cfg in KEYS.items()}
    writej(MANIFEST,manifest)
    report=DEV/'VALIDATION_REPORT.md'
    if report.exists():
        text=report.read_text(encoding='utf-8').rstrip()+'\n\n## Premium 3D held keys\n'
        for tier,name,elements,factor in applied: text+=f'- {tier.title()} — **{name}**: 2D GUI + 3D held/world, {elements} elements, UV factor `{factor:g}`.\n'
        report.write_text(text+f'- SHA1: `{sha1}`\n',encoding='utf-8')
    for row in applied: print(row)
    print('SHA1:',sha1)


if __name__=='__main__': main()
