import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
TOOLS_DIR = PROJECT_ROOT / 'tools'

# tools/ is a plain module folder, not a package
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_DIR))

import build_settings as settings
from build import run


if __name__ == '__main__':
    run(settings.BUILD_PATH, settings.COMMON_PATH,
        settings.SAME_VERSION, settings.__VERSION_CONFIG,
        settings.EXTRA_FILE, settings.EXCLUDE_FILE)
