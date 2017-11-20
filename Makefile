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

install: must_be_root
	$(QUIET)python3 -m pip install "git+https://github.com/reactive-firewall/FetchPublicBlacklists.git#egg=FetchPublicBlacklists"
	$(QUIET)curl -fsSL --tlsv1.2 --url https://github.com/reactive-firewall/FetchPublicBlacklists.git -o ./etc/FetchPublicBlacklists.cfg.template 2>/dev/null || true
	$(QUITE)$(WAIT)
	$(QUITE)$(INSTALL) $(INST_OWN) $(INST_OPTS_CONFIG) ./etc/FetchPublicBlacklists.cfg.template /etc/FetchPublicBlacklists.cfg
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)$(QUIET)python3 -m pip uninstall FetchPublicBlacklists || true
	$(QUITE)rm -f /etc/FetchPublicBlacklists.cfg 2>/dev/null || true
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)python3 -m pip uninstall FetchPublicBlacklists && python -m pip uninstall FetchPublicBlacklists 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

test: cleanup
	$(QUIET)coverage run -p --source=FetchPublicBlacklists -m unittest discover --verbose -s ./tests -t ./ || python3 -m unittest discover --verbose -s ./tests -t ./ || python -m unittest discover --verbose -s ./tests -t ./ || DO_FAIL=exit 2
	$(QUIET)coverage combine 2>/dev/null || true
	$(QUIET)coverage report --include=FetchPublicBlacklists* 2>/dev/null || true
	$(QUIET)$(DO_FAIL)
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v --
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup
	$(QUIET)flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count
	$(QUIET)$(ECHO) "$@: Done."

cleanup:
	$(QUIET)rm -f tests/*.pyc 2>/dev/null || true
	$(QUIET)rm -f tests/*~ 2>/dev/null || true
	$(QUIET)rm -Rf tests/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*.pyc 2>/dev/null || true
	$(QUIET)rm -Rf FetchPublicBlacklists.egg-info 2>/dev/null || true
	$(QUIET)rm -Rf FetchPublicBlacklists/__pycache__ 2>/dev/null || true
	$(QUIET)rm -Rf FetchPublicBlacklists/*/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*~ 2>/dev/null || true
	$(QUIET)rm -f *.pyc 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*/*.pyc 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*/*~ 2>/dev/null || true
	$(QUIET)rm -f *.DS_Store 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f FetchPublicBlacklists/*/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f Fetch_Public_Blacklists.egg-info/* 2>/dev/null || true
	$(QUIET)rmdir Fetch_Public_Blacklists.egg-info 2>/dev/null || true
	$(QUIET)rm -f ./*/*~ 2>/dev/null || true
	$(QUIET)rm -f ./*~ 2>/dev/null || true
	$(QUIET)coverage erase 2>/dev/null || true
	$(QUIET)rm -f ./.coverage 2>/dev/null || true
	$(QUIET)rm -f ./sitecustomize.py 2>/dev/null || true
	$(QUIET)rm -f ./.*~ 2>/dev/null || true
	$(QUIET)rm -Rf ./.tox/ 2>/dev/null || true

clean: cleanup
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

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

/usr/lib/FetchPublicBlacklists/FetchPublicBlacklists/: /usr/lib/FetchPublicBlacklists/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@"
	$(QUITE)$(WAIT)

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;
