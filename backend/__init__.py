"""FastAPI backend wrapping the DCAT-AP-DE quality analyzer.

The core analyzer lives under ``src/`` and uses absolute imports
(``from scoring.service import ...``), so ``src/`` must be on ``sys.path``
before any core module is imported. We add it here, at package import time, so
every backend submodule can simply ``from scoring... import ...``.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
