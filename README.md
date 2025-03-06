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

## Getting Started: The Lazy Way

1. Use [Blender VSCode](https://github.com/JacquesLucke/blender_vscode) to symlink the Blender Extension in `TowerApt/scripts/blender/UsdGameExporter` into your Blender add-on directory and launch a debug session.
2. Run `TowerApt/scripts/pull_textures.py` to download the textures from object storage. It will take a while, I'm hosting them cheaply.
3. Open `TowerApt/src/TowerApt-Source.blend`
4. Check the 'run hooks' checkbox in the `USD GE` viewport panel.
5. Run the USD collection exporter attached to the `TowerAppt` collection.
6. Verify the output in `TowerApt/usd/monolithic/`
