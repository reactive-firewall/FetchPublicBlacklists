# -*- coding: utf-8 -*-


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from . import helpers
except Exception:
    import helpers


try:
    from . import FetchPublicBlacklists
except Exception:
    import FetchPublicBlacklists

try:
    if FetchPublicBlacklists.__name__ is None:
        raise ImportError(str("Failed to import FetchPublicBlacklists"))
    if helpers.__name__ is None:
        raise ImportError(str("Failed to import helpers"))
except Exception:
    raise ImportError(str("Failed to import FetchPublicBlacklists"))

