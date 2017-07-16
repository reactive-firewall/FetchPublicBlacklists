# -*- coding: utf-8 -*-

try:
	try:
		import sys
		import os
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
	except Exception as ImportErr:
		print(str(''))
		print(str(type(ImportErr)))
		print(str(ImportErr))
		print(str((ImportErr.args)))
		print(str(''))
		ImportErr = None
		del ImportErr
		raise ImportError(str("Test module failed completely."))
	try:
		from tests import test_basic
		if test_basic.__name__ is None:
			raise ImportError(str("Test module failed to import even the basic tests."))
	except Exception as impErr:
		print(str(''))
		print(str(type(impErr)))
		print(str(impErr))
		print(str((impErr.args)))
		print(str(''))
		impErr = None
		del impErr
		raise ImportError(str("Test module failed completely."))
		exit(1)
	try:
		from tests import test_advanced
		if test_advanced.__name__ is None:
			raise ImportError(str("Test module failed to import even the more tests."))
	except Exception as impErr:
		print(str(''))
		print(str(type(impErr)))
		print(str(impErr))
		print(str((impErr.args)))
		print(str(''))
		impErr = None
		del impErr
		raise ImportError(str("Test module failed completely."))
		exit(1)
except Exception as badErr:
	print(str(''))
	print(str(type(badErr)))
	print(str(badErr))
	print(str((badErr.args)))
	print(str(''))
	badErr = None
	del badErr
	exit(0)
