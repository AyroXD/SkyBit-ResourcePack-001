# MODEL GUIDE

## Modern item definition
A custom item component such as:

```text
minecraft:item_model = skybit:keys/basic
```

resolves to:

```text
assets/skybit/items/keys/basic.json
```

The item definition then points to one or more models under `assets/skybit/models/`.

## 2D + 3D strategy
Premium physical items use:
- 2D generated icon in GUI
- 3D model in hand, ground, fixed/item-frame and third person

This is selected with `minecraft:select` + `minecraft:display_context`.

## 3D model transforms
Every generated 3D model includes:
- gui
- ground
- fixed
- firstperson_righthand
- firstperson_lefthand
- thirdperson_righthand
- thirdperson_lefthand
- head

## Frostbite Bow
The bow uses `minecraft:range_dispatch` with `minecraft:use_duration` to expose 3 pull stages after the GUI/display-context selection.

## Equipment
Equipment assets:
- `assets/skybit/equipment/stormguard.json`
- `assets/skybit/equipment/emberforged.json`
- `assets/skybit/equipment/voidwarden.json`

Plugin-side armor stacks should set the correct `minecraft:equippable.asset_id`.

## Blockbench workflow
Generated JSON is standard cube-based model JSON and can be imported into Blockbench for hand refinement. When editing:
- keep texture IDs stable
- preserve display transforms unless intentionally retuning
- keep cube count reasonable
- validate UVs after export
