# -*- coding: utf-8 -*-


try:
	import sys
	import os
	if 'FetchPublicBlacklists' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except Exception as ImportErr:
	print(str(type(ImportErr)))
	print(str(ImportErr))
	print(str((ImportErr.args)))
	ImportErr = None
	del ImportErr
	raise ImportError("FetchPublicBlacklists Failed to Import")


try:
	import FetchPublicBlacklists as FetchPublicBlacklists
	if FetchPublicBlacklists.__name__ is None:
		raise ImportError("Failed to import FetchPublicBlacklists.")
except Exception as importErr:
	importErr = None
	del importErr
	raise ImportError("Test module failed to load FetchPublicBlacklists for test.")
	exit(0)

