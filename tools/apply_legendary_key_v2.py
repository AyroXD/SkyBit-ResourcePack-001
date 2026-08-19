from pathlib import Path
import hashlib
import json
import os
import shutil
import zipfile

# Inject the uploaded Legendary Golden Key V2 after the base v6 generator runs.
ROOT = Path(os.getenv('SKYBIT_BUILD_ROOT', 'build-v6'))
PACK = ROOT / 'SkyBitResourcePack'
DEV = ROOT / 'development'
SRC = Path('source/legendary-key-v2')
MODEL_SRC = SRC / 'legendary_golden_key_v2_minecraft.json'
TEXTURE_SRC = SRC / 'legendary_golden_key_v2.png'
RELEASE_ZIP = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11-READY.zip'
ALIAS_ZIP = ROOT / 'SkyBitResourcePack.zip'
SHA_FILE = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11.sha1.txt'
MANIFEST = ROOT / 'release-manifest.json'

MODEL_DST = PACK / 'assets/skybit/models/item/keys/legendary_3d.json'
TEXTURE_DST = PACK / 'assets/skybit/textures/item/keys/legendary_3d.png'
ITEM_DEF_PATHS = [
    PACK / 'assets/skybit/items/keys/legendary.json',
    PACK / 'assets/skybit/items/item/keys/legendary.json',
]


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    if not MODEL_SRC.exists() or not TEXTURE_SRC.exists():
        raise FileNotFoundError('Legendary Golden Key V2 source files are missing')
    if not PACK.exists():
        raise FileNotFoundError(f'Generated pack directory not found: {PACK}')

    TEXTURE_DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEXTURE_SRC, TEXTURE_DST)

    model = json.loads(MODEL_SRC.read_text(encoding='utf-8'))
    model.setdefault('textures', {})['key'] = 'skybit:item/keys/legendary_3d'
    model['textures']['particle'] = 'skybit:item/keys/legendary_3d'
    model['credit'] = 'Legendary Golden Key V2 — SkyBit in-hand model'
    write_json(MODEL_DST, model)

    item_def = {
        'model': {
            'type': 'minecraft:select',
            'property': 'minecraft:display_context',
            'cases': [
                {
                    'when': 'gui',
                    'model': {
                        'type': 'minecraft:model',
                        'model': 'skybit:item/keys/legendary_icon',
                    },
                }
            ],
            'fallback': {
                'type': 'minecraft:model',
                'model': 'skybit:item/keys/legendary_3d',
            },
        },
        'hand_animation_on_swap': False,
        'oversized_in_gui': False,
    }
    for path in ITEM_DEF_PATHS:
        write_json(path, item_def)

    registry = DEV / 'skybit_item_registry.json'
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8'))
        for item in data.get('items', []):
            if item.get('id') == 'skybit:keys/legendary':
                item['render_mode'] = '2d_gui_3d_held'
        data['three_d_held_items'] = 1
        write_json(registry, data)

    integration = DEV / 'skybit-items.yml'
    if integration.exists():
        text = integration.read_text(encoding='utf-8')
        marker = '  - id: "skybit:keys/legendary"'
        if marker in text:
            lines = text.splitlines()
            in_legendary = False
            for i, line in enumerate(lines):
                if line == marker:
                    in_legendary = True
                elif in_legendary and line.startswith('  - id: '):
                    in_legendary = False
                if in_legendary and line.strip().startswith('render_mode:'):
                    lines[i] = '    render_mode: "2d_gui_3d_held"'
            integration.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    if RELEASE_ZIP.exists():
        RELEASE_ZIP.unlink()
    with zipfile.ZipFile(RELEASE_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for file in sorted(PACK.rglob('*')):
            if file.is_file():
                z.write(file, file.relative_to(PACK).as_posix())
    shutil.copy2(RELEASE_ZIP, ALIAS_ZIP)

    sha1 = hashlib.sha1(RELEASE_ZIP.read_bytes()).hexdigest()
    SHA_FILE.write_text(sha1 + '\n', encoding='utf-8')

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    else:
        manifest = {}
    manifest['sha1'] = sha1
    manifest['three_d_held_items'] = 1
    manifest['legendary_key_render_mode'] = '2d_gui_3d_held'
    manifest['legendary_key_model'] = 'skybit:item/keys/legendary_3d'
    write_json(MANIFEST, manifest)

    report = DEV / 'VALIDATION_REPORT.md'
    if report.exists():
        text = report.read_text(encoding='utf-8').rstrip()
        text += '\n\n- Legendary Key: **2D inventory icon + uploaded 3D V2 model in hand/world**.\n'
        text += f'- Legendary Key model: `skybit:item/keys/legendary_3d`\n- Updated SHA1: `{sha1}`\n'
        report.write_text(text, encoding='utf-8')

    print('Applied Legendary Golden Key V2 as held/world model')
    print('SHA1:', sha1)


if __name__ == '__main__':
    main()
