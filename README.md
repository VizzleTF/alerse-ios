# Arcomium for iOS

iOS builds of [Arcomium](https://github.com/VizzleTF/arcomium), an Arc-style browser.
ungoogled-chromium has no iOS build, so this repository applies the arcomium iOS patch
series (`arcomium/patches/series-ios`) to a clean Chromium iOS checkout of the same
version. `arcomium` is a git submodule.

Work in progress. The iOS app syncs with the other Arcomium clients: set it up at
`chrome://arcomium-sync` with the server address and the 24-word sync code.

## Build from source

### Requirements

- Mac with Xcode (iOS SDK and the iOS simulator), about 100 GB of free disk space
- [depot_tools](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html) on `PATH`

### Get Chromium iOS

The version must match `arcomium`'s Chromium version (156.0.8078.79):

```sh
mkdir chromium-ios && cd chromium-ios
fetch --nohooks --no-history ios
cd src && git fetch --depth=1 origin tag 156.0.8078.79 && git checkout 156.0.8078.79
gclient sync --nohooks --no-history -D && gclient runhooks
```

### Build

```sh
git clone --recurse-submodules <this repository> arcomium-ios
python3 arcomium-ios/build.py --src chromium-ios/src
```

`build.py` applies the patches (skipping ones already applied), copies the iOS branding,
writes `out/Sim/args.gn` and builds the `chrome` target. `--device` builds for an iPhone
in `out/Device`; installing on a phone needs your Apple ID in Xcode.

## License

BSD-3-Clause.
