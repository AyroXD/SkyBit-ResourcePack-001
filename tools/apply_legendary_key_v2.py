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
PARTS = Path('source/crate-runtime-fullparts')
RUNTIME = Path('source/SkyBit_Crate_Runtime_V2_Premium.zip')
EXPECTED_RUNTIME_SHA1 = '3bd25066b89a3d4ee948cdca719e30457d8f6fc3'

CRATE_FILES = {
    'basic': (
        'Basic_Crate/basic_crate_v2_premium_minecraft.json',
        'Basic_Crate/basic_crate_v2.png',
        152,
    ),
    'vote': (
        'Vote_Crate/vote_crate_v2_premium_minecraft.json',
        'Vote_Crate/vote_crate_v2.png',
        162,
    ),
    'rare': (
        'Rare_Crate/rare_crate_v2_premium_minecraft.json',
        'Rare_Crate/rare_crate_v2.png',
        162,
    ),
    'epic': (
        'Epic_Crate/epic_crate_v2_premium_minecraft.json',
        'Epic_Crate/epic_crate_v2.png',
        168,
    ),
    'legendary': (
        'Legendary_Crate/legendary_crate_v2_premium_minecraft.json',
        'Legendary_Crate/legendary_crate_v2.png',
        175,
    ),
    'mythic': (
        'Mythic_Crate/mythic_crate_v2_premium_minecraft.json',
        'Mythic_Crate/mythic_crate_v2.png',
        176,
    ),
}
CRATES = tuple(CRATE_FILES)


def writej(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def expected_entries():
    entries = set()
    for model_path, texture_path, _ in CRATE_FILES.values():
        entries.add(model_path)
        entries.add(texture_path)
    return entries


def runtime_ok():
    try:
        if hashlib.sha1(RUNTIME.read_bytes()).hexdigest() != EXPECTED_RUNTIME_SHA1:
            return False
        with zipfile.ZipFile(RUNTIME) as z:
            if z.testzip() is not None:
                return False
            return expected_entries().issubset(set(z.namelist()))
    except (FileNotFoundError, zipfile.BadZipFile):
        return False


def ensure_runtime():
    if runtime_ok():
        return

    files = sorted(PARTS.glob('part*.b64'))
    if len(files) != 12:
        raise FileNotFoundError(f'Expected 12 Premium Crates V2 runtime parts, got {len(files)} in {PARTS}')

    encoded = ''.join(path.read_text(encoding='utf-8').strip() for path in files)
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise RuntimeError('Premium Crates V2 runtime base64 is invalid') from exc

    runtime_sha1 = hashlib.sha1(raw).hexdigest()
    if runtime_sha1 != EXPECTED_RUNTIME_SHA1:
        raise RuntimeError(
            f'Premium Crates V2 runtime SHA1 mismatch: {runtime_sha1} != {EXPECTED_RUNTIME_SHA1}'
        )

    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME.write_bytes(raw)
    if not runtime_ok():
        raise RuntimeError('Reconstructed Premium Crates V2 runtime ZIP is invalid or incomplete')

    print('Verified Premium Crates V2 runtime:', runtime_sha1)


def model_uv_max(model):
    return max(
        [
            float(value)
            for element in model.get('elements', [])
            for face in element.get('faces', {}).values()
            for value in face.get('uv', [])
        ]
        or [0]
    )


def apply_crates():
    if not PACK.exists():
        raise FileNotFoundError(PACK)

    ensure_runtime()
    applied = []
    crate_ids = {f'skybit:crates/{tier}' for tier in CRATES}

    with zipfile.ZipFile(RUNTIME) as z:
        for tier, (source_model, source_texture, expected_elements) in CRATE_FILES.items():
            model = json.loads(z.read(source_model).decode('utf-8'))
            texture = z.read(source_texture)

            elements = len(model.get('elements', []))
            if elements != expected_elements:
                raise RuntimeError(
                    f'{tier} crate element count mismatch: {elements} != {expected_elements}'
                )
            max_uv = model_uv_max(model)
            if max_uv > 16.0001:
                raise RuntimeError(f'{tier} crate UV exceeds 16: {max_uv}')

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

            applied.append((tier, elements, max_uv))

    registry = DEV / 'skybit_item_registry.json'
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8'))
        for item in data.get('items', []):
            iid = item.get('id') or item.get('namespaced_id') or ''
            if iid in crate_ids:
                item['render_mode'] = '3d_crate_v2_premium'
        data['premium_crates_v2'] = list(CRATES)
        writej(registry, data)

    if READY.exists():
        READY.unlink()
    with zipfile.ZipFile(READY, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for file in sorted(PACK.rglob('*')):
            if file.is_file():
                out.write(file, file.relative_to(PACK).as_posix())
    shutil.copy2(READY, ALIAS)

    sha1 = hashlib.sha1(READY.read_bytes()).hexdigest()
    SHA.write_text(sha1 + '\n', encoding='utf-8')

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    manifest['sha1'] = sha1
    manifest['premium_crates_v2'] = {
        tier: {
            'model': f'skybit:item/crates/{tier}_3d',
            'texture': f'skybit:item/crates/{tier}_box',
            'render_mode': '2d_gui_3d_world',
            'elements': expected_elements,
        }
        for tier, (_, _, expected_elements) in CRATE_FILES.items()
    }
    writej(MANIFEST, manifest)

    report = DEV / 'VALIDATION_REPORT.md'
    if report.exists():
        text = report.read_text(encoding='utf-8').rstrip() + '\n\n## Premium Crates V2\n'
        for tier, elements, max_uv in applied:
            text += (
                f'- {tier.title()} Crate V2 Premium: **{elements} elements**, '
                f'2D GUI + replacement 3D crate model, max UV `{max_uv:g}`.\n'
            )
        text += f'- Runtime SHA1: `{EXPECTED_RUNTIME_SHA1}`\n'
        text += f'- Final pack SHA1: `{sha1}`\n'
        report.write_text(text, encoding='utf-8')

    for row in applied:
        print('CRATE', row)
    print('FINAL SHA1:', sha1)


def main():
    apply_keys()
    apply_crates()


if __name__ == '__main__':
    main()
