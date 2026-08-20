from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import zipfile

from apply_premium_keys_core import main as apply_keys

ROOT = Path(os.getenv('SKYBIT_BUILD_ROOT', 'build-v6'))
PACK = ROOT / 'SkyBitResourcePack'
DEV = ROOT / 'development'
READY = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11-READY.zip'
ALIAS = ROOT / 'SkyBitResourcePack.zip'
SHA = ROOT / 'SkyBitResourcePack-v6.0.0-1.21.11.sha1.txt'
MANIFEST = ROOT / 'release-manifest.json'
PARTS = Path('source/crate-runtime-parts')
RUNTIME = Path('source/SkyBit_Crate_Runtime_V2_Premium.zip')
CRATES = ('basic', 'vote', 'rare', 'epic', 'legendary', 'mythic')


def writej(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def expected_entries():
    return {f'{tier}/model.json' for tier in CRATES} | {f'{tier}/texture.png' for tier in CRATES}


def runtime_ok():
    try:
        with zipfile.ZipFile(RUNTIME) as z:
            if z.testzip() is not None:
                return False
            return expected_entries().issubset(set(z.namelist()))
    except (FileNotFoundError, zipfile.BadZipFile):
        return False


def ensure_runtime():
    if runtime_ok():
        return
    files = sorted(PARTS.glob('part*.b64'), key=lambda p: int(''.join(ch for ch in p.stem if ch.isdigit()) or '0'))
    if not files:
        raise FileNotFoundError('Missing source/crate-runtime-parts/part*.b64')
    encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in files)
    encoded += '=' * ((4 - len(encoded) % 4) % 4)
    try:
        raw = base64.b64decode(encoded)
    except Exception as exc:
        raise RuntimeError('Premium crate runtime base64 is invalid') from exc
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME.write_bytes(raw)
    if not runtime_ok():
        raise RuntimeError('Reconstructed Premium Crates V2 runtime ZIP is invalid or incomplete')


def apply_crates():
    if not PACK.exists():
        raise FileNotFoundError(PACK)
    ensure_runtime()
    applied = []
    with zipfile.ZipFile(RUNTIME) as z:
        for tier in CRATES:
            model = json.loads(z.read(f'{tier}/model.json').decode('utf-8'))
            texture = z.read(f'{tier}/texture.png')
            texref = f'skybit:item/crates/{tier}_box'
            textures = model.setdefault('textures', {})
            for key in list(textures):
                textures[key] = texref
            textures['crate'] = texref
            textures['particle'] = texref
            model['credit'] = f'SkyBit {tier.title()} Crate V2 Premium — replacement 3D crate model'
            model_path = PACK / f'assets/skybit/models/item/crates/{tier}_3d.json'
            texture_path = PACK / f'assets/skybit/textures/item/crates/{tier}_box.png'
            writej(model_path, model)
            texture_path.parent.mkdir(parents=True, exist_ok=True)
            texture_path.write_bytes(texture)
            applied.append((tier, len(model.get('elements', []))))

    registry = DEV / 'skybit_item_registry.json'
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8'))
        for item in data.get('items', []):
            iid = item.get('id') or item.get('namespaced_id') or ''
            if iid in {f'skybit:crates/{tier}' for tier in CRATES}:
                item['render_mode'] = '3d_crate_v2_premium'
        data['premium_crates_v2'] = list(CRATES)
        writej(registry, data)

    if READY.exists():
        READY.unlink()
    with zipfile.ZipFile(READY, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for f in sorted(PACK.rglob('*')):
            if f.is_file():
                out.write(f, f.relative_to(PACK).as_posix())
    shutil.copy2(READY, ALIAS)

    sha1 = hashlib.sha1(READY.read_bytes()).hexdigest()
    SHA.write_text(sha1 + '\n', encoding='utf-8')

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    manifest['sha1'] = sha1
    manifest['premium_crates_v2'] = {
        tier: {
            'model': f'skybit:item/crates/{tier}_3d',
            'texture': f'skybit:item/crates/{tier}_box',
            'render_mode': '2d_gui_3d_world'
        }
        for tier in CRATES
    }
    writej(MANIFEST, manifest)

    report = DEV / 'VALIDATION_REPORT.md'
    if report.exists():
        text = report.read_text(encoding='utf-8').rstrip() + '\n\n## Premium Crates V2\n'
        for tier, elements in applied:
            text += f'- {tier.title()} Crate V2 Premium: **{elements} elements**, 2D GUI + replacement 3D crate model.\n'
        report.write_text(text + f'- SHA1: `{sha1}`\n', encoding='utf-8')

    for row in applied:
        print('CRATE', row)
    print('FINAL SHA1:', sha1)


def main():
    apply_keys()
    apply_crates()


if __name__ == '__main__':
    main()
