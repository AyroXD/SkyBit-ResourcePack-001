# SkyBit Ultimate Resource Pack v5.0.0

Production-oriented custom resource pack foundation for **SkyBit Network**.

## Target

- Minecraft Java Edition **26.2**
- Resource Pack format **88.0**
- Namespace: `skybit`
- Vanilla-client friendly: no OptiFine, CIT Resewn, Fabric, Forge, NeoForge or client mod required for core assets.
- Modern item definition system under `assets/skybit/items/...`.

## Technical architecture

Every custom item is addressed by its own namespaced `minecraft:item_model` identifier, for example:

```text
skybit:keys/legendary
```

which maps to:

```text
assets/skybit/items/keys/legendary.json
```

The pack uses the modern item-model definition format and uses `minecraft:select` for 2D GUI vs 3D hand/world presentation. The Frostbite Bow additionally uses `minecraft:range_dispatch` for pull stages.

### Resource pack metadata

`pack.mcmeta` declares exact compatibility with Resource Pack **88.0** using:

```json
"min_format": [88, 0],
"max_format": [88, 0]
```

## Included systems

- 5 VIP / Rank badges
- 6 Keys
- 6 Key fragments
- 6 Crates
- 5 Mine crystals
- SkyCoin + SkyCoin Pouch
- Contracts
- AFK items
- Enchant materials
- Guild, Bounty, Treasure, Event, Achievement and Collection items
- Relics
- Professions
- Renown
- UI icon set
- 5 custom weapons
- Titan Pickaxe
- 3 armor sets / 12 armor items
- Boosters
- Vouchers
- Cosmetics

**TOTAL: 92 / 92**

## Art direction

SkyBit uses one visual language:

**Premium Fantasy + Medieval + Arcane + Clean Minecraft**

The recurring brand motif is the **SB Rune / Sky Crystal**: a split diamond-rune used selectively across premium systems.

Rarity is communicated by **shape, material, geometry, ornament density, color and animation**, not color alone.

## Folder structure

```text
assets/
├── minecraft/
│   └── textures/gui/sprites/widget/
└── skybit/
    ├── items/
    ├── models/item/
    ├── textures/item/
    ├── textures/gui/sprites/tooltip/
    ├── textures/entity/equipment/
    ├── equipment/
    └── lang/
```

## Adding a new item

1. Create the texture under `assets/skybit/textures/item/...`.
2. Create the icon model under `assets/skybit/models/item/..._icon.json`.
3. Create a Blockbench-compatible 3D model if needed under `assets/skybit/models/item/..._3d.json`.
4. Create the modern item definition under `assets/skybit/items/...`.
5. Add it to `skybit_item_registry.json`.
6. Add its translation key to all language files.
7. Add plugin integration entry to `development/integration/skybit-items.yml`.
8. Run validation before publishing.

## Adding a rarity tier

A rarity tier should define:

- material palette
- silhouette/detail rules
- tooltip style
- optional animation behavior
- preferred crystal/rune treatment

Do not add a tier by simply recoloring an existing Mythic or Legendary item.

## Adding a crate tier

A crate family must be developed as one set:

- key
- key fragment
- crate
- mine crystal when applicable

The fragment must visibly belong to the matching key and the crate must reuse the same material/rune language.

## Adding an armor set

1. Add four inventory items.
2. Add `assets/skybit/equipment/<set>.json`.
3. Add humanoid and humanoid leggings textures.
4. Set plugin-side `minecraft:equippable.asset_id` to `skybit:<set>`.
5. Test helmet, chestplate, leggings and boots on a player model.

## Server integration

Use `development/integration/skybit-items.yml`. Core strategy:

```yaml
item-model: skybit:keys/legendary
tooltip-style: skybit:legendary
```

CustomModelData is intentionally not required for the base registry.

## Debugging missing textures

If Minecraft shows purple/black:

1. Check the `minecraft:item_model` ID exactly.
2. Confirm the matching file exists under `assets/skybit/items/`.
3. Open the item definition and verify every `skybit:item/...` model reference.
4. Verify the model references an existing `skybit:item/...` texture.
5. Check JSON parsing.
6. Clear the client's server resource-pack cache before retesting.

## Debugging invalid JSON

Run the validation pipeline or parse every `.json` file before zipping. The release validation report must show zero invalid JSON and zero missing model/texture references.

## QA status

All 92 assets are **GENERATED** and structurally validated.

The pack still requires **NEEDS IN-GAME TESTING** for:
- exact GUI scale/centering
- first/third person transforms
- dropped items and item frames
- armor equipped mapping
- Frostbite Bow pull timing
- animation feel in live gameplay

Do not treat visual QA as complete until it has been tested inside Minecraft Java 26.2.
