from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import zipfile

ROOT = Path(os.getenv('SKYBIT_BUILD_ROOT', 'build-v6'))
PACK = ROOT / 'SkyBitResourcePack'
DEV = ROOT / 'development'
READY = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11-READY.zip'
ALIAS = ROOT / 'SkyBitResourcePack.zip'
SHA = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11.sha1.txt'
MANIFEST = ROOT / 'release-manifest.json'
PACKAGE = Path('source/SkyBit_3_Key_Package.zip')
PACKAGE_PARTS = Path('source/key-package-parts')

KEYS = {
    'rare': {
        'id': 'skybit:keys/rare',
        'name': 'Celestial Azure Key V6 Deluxe',
        'model': '01_Rare_Key_Celestial_Azure/celestial_azure_key_v6_deluxe_minecraft.json',
        'texture': '01_Rare_Key_Celestial_Azure/celestial_azure_key_v6_deluxe.png',
        'display': {
            'thirdperson_righthand': {'rotation': [0, 28, -42], 'translation': [0, 1.6, .5], 'scale': [.44, .44, .44]},
            'thirdperson_lefthand': {'rotation': [0, -28, 42], 'translation': [0, 1.6, .5], 'scale': [.44, .44, .44]},
            'firstperson_righthand': {'rotation': [0, -22, -34], 'translation': [.8, 1.8, .5], 'scale': [.40, .40, .40]},
            'firstperson_lefthand': {'rotation': [0, 22, 34], 'translation': [.8, 1.8, .5], 'scale': [.40, .40, .40]},
            'gui': {'rotation': [18, 30, -28], 'translation': [0, -1.5, 0], 'scale': [.61, .61, .61]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 1, 0], 'scale': [.28, .28, .28]},
            'fixed': {'rotation': [0, 0, -34], 'translation': [0, -.5, 0], 'scale': [.52, .52, .52]},
        },
    },
    'epic': {
        'id': 'skybit:keys/epic',
        'name': 'Cosmic Magenta Key V7 Ultra',
        'model': '02_Epic_Key_Cosmic_Magenta/cosmic_magenta_key_v7_ultra_minecraft.json',
        'texture': '02_Epic_Key_Cosmic_Magenta/cosmic_magenta_key_v7_ultra.png',
        'display': {
            'thirdperson_righthand': {'rotation': [0, 28, -42], 'translation': [0, 1.5, .5], 'scale': [.42, .42, .42]},
            'thirdperson_lefthand': {'rotation': [0, -28, 42], 'translation': [0, 1.5, .5], 'scale': [.42, .42, .42]},
            'firstperson_righthand': {'rotation': [0, -22, -34], 'translation': [.8, 1.7, .5], 'scale': [.38, .38, .38]},
            'firstperson_lefthand': {'rotation': [0, 22, 34], 'translation': [.8, 1.7, .5], 'scale': [.38, .38, .38]},
            'gui': {'rotation': [18, 30, -28], 'translation': [0, -1.5, 0], 'scale': [.60, .60, .60]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 1, 0], 'scale': [.27, .27, .27]},
            'fixed': {'rotation': [0, 0, -34], 'translation': [0, -.5, 0], 'scale': [.50, .50, .50]},
        },
    },
    'legendary': {
        'id': 'skybit:keys/legendary',
        'name': 'Legendary Golden Key V2',
        'source': Path('source/legendary-key-v2'),
        'model': 'legendary_golden_key_v2_minecraft.json',
        'texture': 'legendary_golden_key_v2.png',
        'display': {
            'thirdperson_righthand': {'rotation': [0, 25, -45], 'translation': [0, 2, .5], 'scale': [.52, .52, .52]},
            'thirdperson_lefthand': {'rotation': [0, -25, 45], 'translation': [0, 2, .5], 'scale': [.52, .52, .52]},
            'firstperson_righthand': {'rotation': [0, -20, -35], 'translation': [1, 2.2, .6], 'scale': [.52, .52, .52]},
            'firstperson_lefthand': {'rotation': [0, 20, 35], 'translation': [1, 2.2, .6], 'scale': [.52, .52, .52]},
            'gui': {'rotation': [25, 35, -18], 'translation': [0, -.2, 0], 'scale': [1.03, 1.03, 1.03]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 1.5, 0], 'scale': [.38, .38, .38]},
            'fixed': {'rotation': [0, 0, -35], 'translation': [0, 0, 0], 'scale': [.72, .72, .72]},
        },
    },
    'mythic': {
        'id': 'skybit:keys/mythic',
        'name': 'Astral Empress Key V8',
        'model': '03_Mythic_Key_Astral_Empress/astral_empress_key_v8_minecraft.json',
        'texture': '03_Mythic_Key_Astral_Empress/astral_empress_key_v8.png',
        'display': {
            'thirdperson_righthand': {'rotation': [0, 28, -42], 'translation': [0, 1.4, .5], 'scale': [.40, .40, .40]},
            'thirdperson_lefthand': {'rotation': [0, -28, 42], 'translation': [0, 1.4, .5], 'scale': [.40, .40, .40]},
            'firstperson_righthand': {'rotation': [0, -22, -34], 'translation': [.7, 1.6, .5], 'scale': [.36, .36, .36]},
            'firstperson_lefthand': {'rotation': [0, 22, 34], 'translation': [.7, 1.6, .5], 'scale': [.36, .36, .36]},
            'gui': {'rotation': [18, 30, -28], 'translation': [0, -1.5, 0], 'scale': [.60, .60, .60]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 1, 0], 'scale': [.26, .26, .26]},
            'fixed': {'rotation': [0, 0, -34], 'translation': [0, -.5, 0], 'scale': [.48, .48, .48]},
        },
    },
}


def writej(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def package_is_valid():
    try:
        with zipfile.ZipFile(PACKAGE) as archive:
            return archive.testzip() is None
    except (FileNotFoundError, zipfile.BadZipFile):
        return False


def ensure_package():
    if package_is_valid():
        return

    parts = [PACKAGE_PARTS / f'part{i}.b64' for i in range(1, 5)]
    missing = [str(path) for path in parts if not path.exists()]
    if missing:
        raise FileNotFoundError('Missing package parts: ' + ', '.join(missing))

    encoded = ''.join(path.read_text(encoding='utf-8').strip() for path in parts)
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise RuntimeError('Premium key package base64 data is invalid') from exc

    PACKAGE.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE.write_bytes(raw)

    try:
        with zipfile.ZipFile(PACKAGE) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f'Corrupt file inside premium key package: {bad}')
            expected = {
                KEYS['rare']['model'], KEYS['rare']['texture'],
                KEYS['epic']['model'], KEYS['epic']['texture'],
                KEYS['mythic']['model'], KEYS['mythic']['texture'],
            }
            names = set(archive.namelist())
            missing_entries = sorted(expected - names)
            if missing_entries:
                raise RuntimeError('Premium key package is missing: ' + ', '.join(missing_entries))
    except zipfile.BadZipFile as exc:
        raise RuntimeError('Reconstructed premium key package is not a valid ZIP') from exc

    print('Reconstructed verified source/SkyBit_3_Key_Package.zip from package parts')


def fix_uv(model):
    vals = [
        float(value)
        for element in model.get('elements', [])
        for face in element.get('faces', {}).values()
        for value in face.get('uv', [])
    ]
    maximum = max(vals or [0])
    factor = 1 if maximum <= 16.0001 or maximum == 0 else 16.0 / maximum
    if factor != 1:
        for element in model.get('elements', []):
            for face in element.get('faces', {}).values():
                if face.get('uv'):
                    face['uv'] = [round(float(value) * factor, 4) for value in face['uv']]
    return factor


def itemdef(tier):
    return {
        'model': {
            'type': 'minecraft:select',
            'property': 'minecraft:display_context',
            'cases': [{
                'when': 'gui',
                'model': {
                    'type': 'minecraft:model',
                    'model': f'skybit:item/keys/{tier}_icon',
                },
            }],
            'fallback': {
                'type': 'minecraft:model',
                'model': f'skybit:item/keys/{tier}_3d',
            },
        },
        'hand_animation_on_swap': False,
        'oversized_in_gui': False,
    }


def patch_yml(path, ids):
    if not path.exists():
        return
    lines = path.read_text(encoding='utf-8').splitlines()
    current = None
    for index, line in enumerate(lines):
        if line.startswith('  - id: '):
            current = line.split('"', 2)[1] if '"' in line else None
        elif current in ids and line.strip().startswith('render_mode:'):
            lines[index] = '    render_mode: "2d_gui_3d_held"'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    if not PACK.exists():
        raise FileNotFoundError(PACK)

    ensure_package()
    applied = []
    ids = set()

    with zipfile.ZipFile(PACKAGE) as package:
        for tier, config in KEYS.items():
            if 'source' in config:
                model = json.loads((config['source'] / config['model']).read_text(encoding='utf-8'))
                texture = (config['source'] / config['texture']).read_bytes()
            else:
                model = json.loads(package.read(config['model']))
                texture = package.read(config['texture'])

            factor = fix_uv(model)
            model.setdefault('textures', {})['key'] = f'skybit:item/keys/{tier}_3d'
            model['textures']['particle'] = f'skybit:item/keys/{tier}_3d'
            model['display'] = config['display']
            model['credit'] = config['name'] + ' — SkyBit 3D held/world model'

            model_dst = PACK / f'assets/skybit/models/item/keys/{tier}_3d.json'
            texture_dst = PACK / f'assets/skybit/textures/item/keys/{tier}_3d.png'
            writej(model_dst, model)
            texture_dst.parent.mkdir(parents=True, exist_ok=True)
            texture_dst.write_bytes(texture)

            definition = itemdef(tier)
            writej(PACK / f'assets/skybit/items/keys/{tier}.json', definition)
            writej(PACK / f'assets/skybit/items/item/keys/{tier}.json', definition)

            ids.add(config['id'])
            applied.append((tier, config['name'], len(model.get('elements', [])), factor))

    registry = DEV / 'skybit_item_registry.json'
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8'))
        for item in data.get('items', []):
            if (item.get('id') or item.get('namespaced_id')) in ids:
                item['render_mode'] = '2d_gui_3d_held'
        data['three_d_held_items'] = 4
        data['three_d_held_key_ids'] = sorted(ids)
        writej(registry, data)

    patch_yml(DEV / 'skybit-items.yml', ids)
    patch_yml(DEV / 'integration/skybit-items.yml', ids)

    if READY.exists():
        READY.unlink()
    with zipfile.ZipFile(READY, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in sorted(PACK.rglob('*')):
            if file.is_file():
                archive.write(file, file.relative_to(PACK).as_posix())
    shutil.copy2(READY, ALIAS)

    sha1 = hashlib.sha1(READY.read_bytes()).hexdigest()
    SHA.write_text(sha1 + '\n', encoding='utf-8')

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    manifest['sha1'] = sha1
    manifest['three_d_held_items'] = 4
    manifest['three_d_held_keys'] = {
        tier: {
            'name': config['name'],
            'render_mode': '2d_gui_3d_held',
            'model': f'skybit:item/keys/{tier}_3d',
        }
        for tier, config in KEYS.items()
    }
    writej(MANIFEST, manifest)

    report = DEV / 'VALIDATION_REPORT.md'
    if report.exists():
        text = report.read_text(encoding='utf-8').rstrip() + '\n\n## Premium 3D held keys\n'
        for tier, name, elements, factor in applied:
            text += f'- {tier.title()} — **{name}**: 2D GUI + 3D held/world, {elements} elements, UV factor `{factor:g}`.\n'
        report.write_text(text + f'- SHA1: `{sha1}`\n', encoding='utf-8')

    for result in applied:
        print(result)
    print('SHA1:', sha1)


if __name__ == '__main__':
    main()
