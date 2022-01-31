import os
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASEDIR, "static")