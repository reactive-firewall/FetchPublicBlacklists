#!/usr/bin/env make -f

# Since this Makefile is handwriten and maintained, much of this is verbosely typed out for clearity

ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(MAKE)" ""
	MAKE=make
endif

ifeq "$(INSTALL)" ""
	INSTALL=install
	ifeq "$(INST_OWN)" ""
		INST_OWN=-o root -g staff
	endif
	ifeq "$(INST_OPTS)" ""
		INST_OPTS=-m 755
	endif
	ifeq "$(INST_OPTS_CONFIG)" ""
		INST_OPTS_CONFIG=-m 644
	endif
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
endif

PHONY: must_be_root

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install: /usr/local/bin/ /usr/lib/FetchPublicBlacklists/code/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) ./code/core.py /usr/lib/FetchPublicBlacklists/code/
	$(QUITE) $(WAIT)
	$(QUITE)$(LINK) /usr/lib/FetchPublicBlacklists/code/core.py /usr/local/bin/FetchPublicBlacklists.py
	$(QUITE) $(WAIT)
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) ./code/helpers.py /usr/lib/FetchPublicBlacklists/code/helpers.py
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) ./code/__init__.py /usr/lib/FetchPublicBlacklists/code/__init__.py
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS_CONFIG) ./etc/FetchPublicBlacklists.cfg.template /etc/FetchPublicBlacklists.cfg
	$(QUITE) $(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)rm -f /usr/lib/FetchPublicBlacklists/code/core.py 2>/dev/null || true
	$(QUITE)rm -f /usr/lib/FetchPublicBlacklists/code/helpers.py 2>/dev/null || true
	$(QUITE)rm -f /usr/lib/FetchPublicBlacklists/code/__init__.py 2>/dev/null || true
	$(QUITE)rm -f /usr/lib/FetchPublicBlacklists/code/*.pyc 2>/dev/null || true
	$(QUITE)rm -Rf /usr/lib/FetchPublicBlacklists/code/ 2>/dev/null || true
	$(QUITE)rm -f /etc/FetchPublicBlacklists.cfg 2>/dev/null || true
	$(QUITE)unlink /usr/local/bin/FetchPublicBlacklists.py 2>/dev/null || true
	$(QUITE) $(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)$(ECHO) "$@: Done."

test:
	$(QUIET)python -m unittest tests.test_basic
	$(QUIET)python -m unittest tests.test_advanced
	$(QUIET)$(ECHO) "$@: Done."

clean:
	$(QUIET)$(MAKE) -C ./docs/ -f Makefile clean 2>/dev/null
	$(QUIET)rm -f tests/*.pyc 2>/dev/null
	$(QUIET)rm -f code/*.pyc 2>/dev/null
	$(QUIET)rm -f *.pyc 2>/dev/null
	$(QUIET)$(ECHO) "$@: Done."

must_be_root:
	runner=`whoami` ; \
	if test $$runner != "root" ; then echo "You are not root." ; exit 1 ; fi

/usr/local/: /usr/ must_be_root
	$(QUITE)$(INSTALL) $(INST_OWN) $(INST_OPTS) -d "$@"
	$(QUITE)$(WAIT)

/usr/local/bin/: /usr/local/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@"
	$(QUITE)$(WAIT)

/usr/lib/: /usr/ must_be_root
	$(QUITE)$(INSTALL) $(INST_OWN) $(INST_OPTS) -d "$@"
	$(QUITE)$(WAIT)

/usr/lib/FetchPublicBlacklists/: /usr/lib/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@"
	$(QUITE)$(WAIT)

/usr/lib/FetchPublicBlacklists/code/: /usr/lib/FetchPublicBlacklists/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@"
	$(QUITE)$(WAIT)

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;
