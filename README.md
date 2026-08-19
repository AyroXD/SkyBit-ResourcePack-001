# SkyBit Resource Pack

Official custom resource pack for **SkyBit Network**.

## Current version

**v3.7.0** — Minecraft Java **1.21.11** / resource-pack format **75**.

### Visual Overhaul

- complete texture refresh with unified SkyBit palettes and material atlases
- new `pack.png` and SkyBit Network branding
- improved 3D weapons, tools, keys, crystals and crate models
- 3D inventory models for Stormguard, Emberforged and Voidwarden armor pieces
- premium Legendary Crate crown-style silhouette
- unique Mythic Crate void horns/glow styling
- new AFK Zone visual core used by SkyBitCore 3.7.0

### Direct resource-pack URL

```text
https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.7.0-READY.zip
```

### SHA1

```text
5a5474e4facb71a3f71c49cf7def766790110533
```

### SkyBitCore

```text
/sba pack seturl https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.7.0-READY.zip 5a5474e4facb71a3f71c49cf7def766790110533
/sba pack send all
```

### server.properties

```properties
resource-pack=https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.7.0-READY.zip
resource-pack-sha1=5a5474e4facb71a3f71c49cf7def766790110533
require-resource-pack=false
```

## Build

GitHub Actions generates the current pack from `tools/generate_pack.py`, then applies the 3.7 texture/branding and custom-model passes. The generated ZIP and SHA1 are validated before being committed.

Older generated pack files are removed so `main` exposes only the current v3.7.0 release.
