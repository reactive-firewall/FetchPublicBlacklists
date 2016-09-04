Fetch Public Blacklists Tool
============================
.. image:: https://badge.fury.io/gh/reactive-firewall%2FFetchPublicBlacklists.svg

A tool to fetch public blacklists for other tools.

.. image:: https://travis-ci.org/reactive-firewall/FetchPublicBlacklists.svg?branch=master
    :target: https://travis-ci.org/reactive-firewall/FetchPublicBlacklists

.. image:: https://reposs.herokuapp.com/?path=/reactive-firewall/FetchPublicBlacklists

10 minute Quick Start
===================== 

Download
--------

Download the project .zip and unarchive it.  

Install
-------

Run the command sudo make install from within the unarchive project folder.

Configure
---------

Using your favorite editor, open the configuration template /etc/FetchPublicBlacklists.cfg

Configure the 'urls' setting to a comma-separated-list of blacklist source urls (file:///, https:// ...etc...)

The format of the blacklist is ignored and assumed to contain multiple CIDRs and IPs in IPv4 dot notation (i.e. 127.2.3.4/32 or 127.2.3.4)

Customize any settings to fit your deployment environment.

Usage
------

Fetch Public Blacklists [-h] [--dry-run] [--config CONFIG] [--tmp-dir]
                               [--hosts-deny] [--snort-deny]
                               [--snort-blacklist SNORT_BLACKLIST]
                               [--nginx-deny]
                               [--nginx-blacklist NGINX_BLACKLIST]
                               [--splunk-deny]
                               [--splunk-blacklist SPLUNK_BLACKLIST]
                               [--iptables-deny]
                               [--iptables-blacklist IPTABLES_BLACKLIST]
                               [--pf-deny] [--pf-blacklist PF_BLACKLIST]
                               [--exim4-deny]
                               [--exim4-blacklist EXIM4_BLACKLIST] [--display]
                               [-V]

Process some public online blacklists.

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             only show what would be done
  --config CONFIG       where is the config file
  --tmp-dir             where should temp files go
  --hosts-deny          generate a host.deny file from the ip list
  --snort-deny          enable snort blacklist ip reputation file
  --snort-blacklist SNORT_BLACKLIST
                        where to put the snort blacklist ip reputation file
  --nginx-deny          enable nginx blacklist ip file
  --nginx-blacklist NGINX_BLACKLIST
                        where to put the nginx ip blacklist config file
  --splunk-deny         enable splunk blacklist ip file
  --splunk-blacklist SPLUNK_BLACKLIST
                        where to put the EXPERIMENTAL splunk blacklist file
  --iptables-deny       enable a list of iptables blacklist rules
  --iptables-blacklist IPTABLES_BLACKLIST
                        iptables-save style list of iptables blacklist rules
  --pf-deny             enable a list of pf blacklist rules
  --pf-blacklist PF_BLACKLIST
                        pf config style list of pf blacklist rules
  --exim4-deny          enable a exim4 blacklist file
  --exim4-blacklist EXIM4_BLACKLIST
                        exim4 local hosts blacklist
  --display             just print the ip list
  -V, --version         show program's version number and exit


Simple Example
-------
Updates hosts.deny file with any configured URLs
.. code-block:: bash
   :linenos:

	export PATH=/usr/local/bin/:${PATH} ;
	FetchPublicBlacklists.py --hosts-deny



Custom Example
--------------
Updates hosts.deny file with any logged IPs in the log file /var/log/network_attackers_custom_blacklist.log

Configuration
.. code-block:: plain
   :linenos:

	[URL Sources]
	urls = file:///etc/hosts.deny, file:///var/log/network_attackers_custom_blacklist.log

Usage
.. code-block:: bash
   :linenos:

	export PATH=/usr/local/bin/:${PATH} ;
	FetchPublicBlacklists.py --hosts-deny --iptables-deny

Caveat: the log file needs to already exist.


TODO:
=====
- add detailed docs (not just quick start and --help)
- add installers (not just make install)
- increase test coverage 
- (optional) daemon mode?
- (optional) reputation threshold feature?

