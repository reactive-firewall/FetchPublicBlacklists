# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
        from . import helpers
except Exception:
        import helpers
try:
        from . import core
except Exception:
        import core