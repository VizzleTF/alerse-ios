#!/usr/bin/env python3
"""Build Arcomium for iOS: Chromium iOS + the Arcomium iOS patch series.

ungoogled-chromium has no iOS build, so this applies arcomium/patches/series-ios
to a clean Chromium iOS checkout of the same version, copies the iOS branding
files, writes args.gn and builds the app.

  python3 build.py --src ~/chromium-ios/src            # simulator build
  python3 build.py --src ~/chromium-ios/src --device   # iPhone build
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / 'arcomium'
PATCHES = CORE / 'patches'
BRANDING = CORE / 'branding' / 'ios'

ARGS = """\
target_os = "ios"
target_cpu = "arm64"
target_environment = "{environment}"
is_debug = false
is_component_build = false
symbol_level = 0
enable_precompiled_headers = false
use_remoteexec = false
# Unofficial builds otherwise turn on the experiments of
# fieldtrial_testing_config.json, which break sync with an Arcomium server.
disable_fieldtrial_testing_config = true
ios_enable_code_signing = {signing}
"""


def read_series(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith('#')]


def git(src, *args, check=True):
    return subprocess.run(['git', *args], cwd=src, check=check,
                          capture_output=True, text=True)


def apply_patches(src):
    for name in read_series(PATCHES / 'series-ios'):
        patch = str(PATCHES / name)
        if git(src, 'apply', '--check', patch, check=False).returncode == 0:
            git(src, 'apply', patch)
            print(f'applied {name}')
        elif git(src, 'apply', '--check', '--reverse', patch, check=False).returncode == 0:
            print(f'already applied {name}')
        else:
            sys.exit(f'{name} does not apply; is the checkout the right version?')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--src', type=Path, required=True,
                        help='the src directory of a Chromium iOS checkout')
    parser.add_argument('--device', action='store_true',
                        help='build for an iPhone instead of the simulator')
    parser.add_argument('--out', help='output directory, under src')
    parser.add_argument('--gen-only', action='store_true',
                        help='patch and generate the build, but do not build')
    args = parser.parse_args()
    src = args.src.expanduser().resolve()

    apply_patches(src)
    # Arcomium's own source files are copied over the tree, not patched in.
    shutil.copytree(CORE / 'src', src, dirs_exist_ok=True)
    shutil.copytree(BRANDING, src / 'ios', dirs_exist_ok=True)
    # Renaming the product moves hundreds of translations: a script, not a patch.
    subprocess.run([sys.executable, str(CORE / 'tools' / 'rename_product.py'), str(src)],
                   check=True)

    out = args.out or ('out/Device' if args.device else 'out/Sim')
    (src / out).mkdir(parents=True, exist_ok=True)
    (src / out / 'args.gn').write_text(ARGS.format(
        environment='device' if args.device else 'simulator',
        signing='true' if args.device else 'false'), encoding='utf-8')
    subprocess.run(['gn', 'gen', out], cwd=src, check=True)
    if args.gen_only:
        return 0
    return subprocess.run(['autoninja', '-C', out, 'chrome'], cwd=src).returncode


if __name__ == '__main__':
    sys.exit(main())
