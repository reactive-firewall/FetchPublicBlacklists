#!/usr/bin/env make -f

ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
endif

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install:
	$(QUIET)$(ECHO) "$@: Done."

test:
	$(QUIET)python -m unittest tests.test_basic
	$(QUIET)python -m unittest tests.test_advanced

clean:
	$(QUIET)rm -vf tests/*.pyc 2>/dev/null
	$(QUIET)rm -vf code/*.pyc 2>/dev/null
	$(QUIET)rm -vf *.pyc 2>/dev/null


%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;