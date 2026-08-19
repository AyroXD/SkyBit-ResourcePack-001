from pathlib import Path
import json
import shutil

ROOT = Path("build/SkyBit-ResourcePack")
META = ROOT / "pack.mcmeta"
ITEMS = ROOT / "assets/skybit/items"

# Minecraft 1.21.9+ (resource-pack format >= 65) requires min_format and
# max_format in pack.mcmeta. 1.21.11 uses resource-pack format 75.0.
data = json.loads(META.read_text(encoding="utf-8"))
pack = data.setdefault("pack", {})
pack["pack_format"] = 75
pack["min_format"] = 75
pack["max_format"] = 75
META.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Compatibility aliases for plugins/configs that still use the old-looking
# skybit:item/<path> value as minecraft:item_model. Since 1.21.4 the value
# points to assets/<namespace>/items/<path>.json, so keep aliases under item/.
if ITEMS.exists():
    canonical = [p for p in ITEMS.rglob("*.json") if "item" not in p.relative_to(ITEMS).parts[:1]]
    for src in canonical:
        rel = src.relative_to(ITEMS)
        dst = ITEMS / "item" / rel
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

print("Applied Minecraft 1.21.11 resource-pack metadata + item-model compatibility aliases")
