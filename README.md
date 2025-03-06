# Tower Apt. USD Example

**TL;DR:** An apartment, made in Blender, for testing USD workflows. Plus a bunch of other things. Larger than a bare cube, smaller than a full film/VFX scene, loosely aimed at game development.

## Repo Map

```Tree
┌ usdExample_TowerApt
├─ TowerApt
│  ├─ scripts
│  │  ├─ blender
│  │  │  └─ UsdGameExporter     ← Blender extension for wrangling USD data
│  │  └─ pull_textures.py       ← Downloads ~1gb of CC0 textures 
│  │
│  ├─ src
│  │  ├─ tex                    ← where textures are downloaded to
│  │  ├─ texture_catalog.json   ← source map of textures used
│  │  └─ TowerApt-Source.blend  ← Primary Source File
│  │
│  └─ usd                       ← Where the USD files are exported to
│
└ README.md
```

## License

License files are loosely co-located with the content they cover, but the overal licensing posture here is that everything that *can* be CC0 *is* CC0. The code that touches Blender's API is GPL2 (because it has to be), but the rest is meant to be fully unencumbered.

In short: Please steal.

