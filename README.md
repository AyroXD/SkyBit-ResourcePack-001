# SkyBit Resource Pack

Custom resource pack for **SkyBit Network**.

## Current version

**v3.2.0** — Minecraft Java **1.21.11** / resource-pack format **75**.

### Direct resource-pack URL

```text
https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.2.0-READY.zip
```

### SHA1

```text
66a3757bc3cdcab79114f27ce39efcab91f3c7b6
```

### server.properties example

```properties
resource-pack=https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.2.0-READY.zip
resource-pack-sha1=66a3757bc3cdcab79114f27ce39efcab91f3c7b6
require-resource-pack=false
```

Or with SkyBitCore:

```text
/sba pack seturl https://raw.githubusercontent.com/AyroXD/SkyBit-ResourcePack-001/main/SkyBit-ResourcePack-v3.2.0-READY.zip 66a3757bc3cdcab79114f27ce39efcab91f3c7b6
/sba pack send all
```

## Build

The pack is generated reproducibly by `tools/generate_pack.py` and GitHub Actions automatically commits the generated ZIP and SHA1 file.
