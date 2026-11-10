<p align="center">
  <img src="https://raw.githubusercontent.com/VizzleTF/alerse/main/artwork/alerse_256.png" width="120" alt="The Alerse icon">
</p>

<h1 align="center">Alerse for iOS</h1>

<p align="center">The iPhone build of Alerse: its sync on Chromium for iOS, work in progress.</p>

iOS builds of [Alerse](https://github.com/VizzleTF/alerse), an Arc-style browser. The
app built here still has the project's earlier name: the `alerse` submodule is pinned at
0.1.1, before the rename; the core's iOS series names it Alerse
(`ios/alerse-ios-name.patch`) once this repository moves to it.
ungoogled-chromium has no iOS build, so this repository applies the core's iOS patch
series (`alerse/patches/series-ios`) to a clean Chromium iOS checkout of the same
version. `alerse` is a git submodule.

Work in progress. The iOS app syncs with the other Alerse clients: set it up at
its sync page (`chrome://arcomium-sync` in the pinned 0.1.1) with the server address and the 24-word sync code.
The `alerse` submodule is pinned at 0.1.1 (Chromium 156), and the iOS series has no
`sync/e2e-before-data.patch`: the app does not hold data back until the chain's
passphrase is set. Start a sync chain on a desktop and only join it from the iPhone.

## Build from source

### Requirements

- Mac with Xcode (iOS SDK and the iOS simulator), about 100 GB of free disk space
- [depot_tools](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html) on `PATH`

### Get Chromium iOS

The version must match `alerse`'s Chromium version (156.0.8078.79):

```sh
mkdir chromium-ios && cd chromium-ios
fetch --nohooks --no-history ios
cd src && git fetch --depth=1 origin tag 156.0.8078.79 && git checkout 156.0.8078.79
gclient sync --nohooks --no-history -D && gclient runhooks
```

### Build

```sh
git clone --recurse-submodules <this repository> alerse-ios
python3 alerse-ios/build.py --src chromium-ios/src
```

`build.py` applies the patches (skipping ones already applied), copies the iOS branding,
writes `out/Sim/args.gn` and builds the `chrome` target. `--device` builds for an iPhone
in `out/Device`; installing on a phone needs your Apple ID in Xcode. `--gen-only` patches
the tree and generates the build without building it.

The build sets `disable_fieldtrial_testing_config = true`. A non-official build would
otherwise turn on the experiments of `fieldtrial_testing_config.json`, among them one
whose checks stop Alerse's sync on iOS (`kSyncUsePropagatedAccessToken`, enabled for
iOS in that file; its `CHECK` in `components/sync/service/sync_auth_manager.cc` does not
hold when Alerse hands sync its token itself).

The iOS series takes the platform-independent sync client
(`sync/alerse-sync-core.patch`) from the desktop series and adds the iOS wiring, the
`chrome://alerse-sync` page and the name. The page accepts any `http` or `https`
server address; the desktop page takes plain `http` only for a server on the same
computer.

## License

BSD-3-Clause.
