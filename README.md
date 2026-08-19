# SkyBit Resource Pack

Official custom resource pack for **SkyBit Network**.

## Current version

**v4.0.0 Premium** — Minecraft Java **1.21.11** / resource-pack format **75**.

### Premium Custom Items overhaul

v4 replaces the old generated placeholders with a complete original SkyBit item set aimed at the visual quality of modern premium Minecraft networks:

- **92 canonical custom items** generated in one consistent style
- separate **2D inventory/ground icons** and **3D hand/fixed models** using the modern `minecraft:display_context` item-model system
- premium rank badges: **VIP, Knight, Baron, King, Emperor**
- **Basic, Rare, Epic, Legendary, Mythic and Vote** keys + key fragments
- matching premium 3D crates, with enhanced Legendary and Mythic silhouettes
- AFK Core, SkyCoins, contracts, enchant items, guild/bounty items, relics, professions, renown medals and UI icons
- custom SkyBit weapons, tools and armor inventory models
- extra modern-server items: boosters, vouchers and cosmetics tokens
- compatibility aliases under `skybit:item/...` for plugins/configs that use the older-looking item-model path
- custom SkyBit GUI button styling, languages and pack branding

### Modern item rendering

The pack uses Minecraft's data-driven item model format. Inventory and dropped-item contexts use a clean 2D icon, while hand, fixed/item-frame and other contexts fall back to the 3D model. This keeps menus readable while world/hand items look custom.

### Direct resource-pack URL

```text
https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v4.0.0-READY.zip
```

### SHA1

```text
241b2924c310433c95067c008cd56385030920b7
```

### SkyBitCore

```text
/sba pack seturl https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v4.0.0-READY.zip 241b2924c310433c95067c008cd56385030920b7
/sba pack send all
```

### server.properties

```properties
resource-pack=https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v4.0.0-READY.zip
resource-pack-sha1=241b2924c310433c95067c008cd56385030920b7
require-resource-pack=false
```

### Important item-model IDs

```text
skybit:vip/vip_badge
skybit:vip/knight_badge
skybit:vip/baron_badge
skybit:vip/king_badge
skybit:vip/emperor_badge

skybit:keys/basic
skybit:keys/rare
skybit:keys/epic
skybit:keys/legendary
skybit:keys/mythic
skybit:keys/vote

skybit:crates/basic
skybit:crates/rare
skybit:crates/epic
skybit:crates/legendary
skybit:crates/mythic
skybit:crates/vote

skybit:afk/beacon
skybit:currency/skycoin
```

If a plugin currently uses values such as `skybit:item/crates/mythic`, v4 also generates matching compatibility definitions.

## Build

GitHub Actions runs `tools/generate_premium40.py`, validates the generated item definitions and packages the result as `SkyBit-ResourcePack-v4.0.0-READY.zip` with a SHA1 file.

The previous v3.7 release remains in the repository as a rollback while v4 is tested on the server.
