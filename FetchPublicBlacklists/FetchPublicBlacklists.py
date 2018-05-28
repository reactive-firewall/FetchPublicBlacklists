#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from . import helpers
except Exception:
    import helpers


def parseArgs():
    parser = argparse.ArgumentParser(
        prog='Fetch Public Blacklists',
        description='Process some public online blacklists.'
    )
    parser.add_argument(
        '--dry-run',
        default=False,
        action='store_true',
        help='only show what would be done'
    )
    parser.add_argument(
        '--config',
        default='/etc/FetchPublicBlacklists.cfg',
        help='where is the config file'
    )
    parser.add_argument(
        '--tmp-dir',
        default=False,
        action='store_true',
        help='where should temp files go'
    )
    parser.add_argument(
        '--hosts-deny',
        default=False,
        action='store_true',
        help='generate a host.deny file from the ip list'
    )
    parser.add_argument(
        '--snort-deny',
        default=False,
        action='store_true',
        help='enable snort blacklist ip reputation file'
    )
    parser.add_argument(
        '--snort-blacklist',
        default='/etc/snort/rules/black_list.rules',
        help='where to put the snort blacklist ip reputation file'
    )
    parser.add_argument(
        '--nginx-deny',
        default=False,
        action='store_true',
        help='enable nginx blacklist ip file'
    )
    parser.add_argument(
        '--nginx-blacklist',
        default='/etc/nginx/conf-available/blacklist.conf',
        help='where to put the nginx ip blacklist config file'
    )
    parser.add_argument(
        '--splunk-deny',
        default=False,
        action='store_true',
        help='enable splunk blacklist ip file'
    )
    parser.add_argument(
        '--splunk-blacklist',
        default='/opt/splunk/etc/system/local/inputs.conf',
        help='where to put the EXPERIMENTAL splunk blacklist file'
    )
    parser.add_argument(
        '--iptables-deny',
        default=False,
        action='store_true',
        help='enable a list of iptables blacklist rules'
    )
    parser.add_argument(
        '--iptables-blacklist',
        default='/etc/blacklist.rules',
        help='iptables-save style list of iptables blacklist rules'
    )
    parser.add_argument(
        '--pf-deny',
        default=False,
        action='store_true',
        help='enable a list of pf blacklist rules'
    )
    parser.add_argument(
        '--pf-blacklist',
        default='/etc/blacklist_pf.conf',
        help='pf config style list of pf blacklist rules'
    )
    parser.add_argument(
        '--exim4-deny',
        default=False,
        action='store_true',
        help='enable a exim4 blacklist file'
    )
    parser.add_argument(
        '--exim4-blacklist',
        default='/etc/exim4/local_host_blacklist',
        help='exim4 local hosts blacklist'
    )
    parser.add_argument(
        '--display',
        default=False,
        action='store_true',
        help='just print the ip list'
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='%(prog)s 0.3.3'
    )
    args = parser.parse_args()
    return args


def readFile(somefile):
    read_data = None
    theReadPath = str(somefile)
    with open(theReadPath, 'r') as f:
        read_data = f.read()
    f.close()
    return read_data


def writeFile(somefile, somedata):
    theWritePath = str(somefile)
    try:
        with open(theWritePath, 'r+') as f:
            f.write(somedata)
        f.close()
    except Exception:
        try:
            f.close()
        except Exception:
            return False
        return False
    return True


def appendFile(somefile, somedata):
    theWritePath = str(somefile)
    try:
        with open(theWritePath, 'a') as f:
            f.write(somedata)
            f.write('\n')
        f.close()
    except Exception:
        try:
            f.close()
        except Exception:
            return False
        return False
    return True


def getBlackList(someURL, outFile):
    import urllib
    try:
        tempfile = urllib.FancyURLopener()
    except Exception:
        import urllib.request
        tempfile = urllib.request.FancyURLopener()
    tempfile.retrieve(someURL, outFile)
    return True


# TODO MOVE THIS TO A PY LIB
def extractRegexPattern(theInput_Str, theInputPattern):
    import re
    sourceStr = str(theInput_Str)
    prog = re.compile(theInputPattern)
    theList = prog.findall(sourceStr)
    return theList


def extractIPv4Addr(theInputStr):
    return extractRegexPattern(theInputStr, "(?:(?:[[:print:]]*){0,1}(?P<IP>(?:(?:[0-9]{1,3}[\.]{1}){3}(?:[0-9]{1,3}){1}){1})+(?:[[:print:]]*){0,1})+")  # noqa E401


def extractConfigItem(someSection='URL Sources', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):  # noqa
    try:
        import ConfigParser as configparser
    except Exception:
        import configparser
    config = configparser.ConfigParser()
    try:
        config.read(thePath)
        return config.get(someSection, theInputKey)
    except Exception:
        return None
    return None


def extractConfigBool(someSection='Options', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):
    try:
        import ConfigParser as configparser
    except Exception:
        import configparser
    config = configparser.ConfigParser()
    try:
        config.read(thePath)
        return config.getbloolean(someSection, theInputKey)
    except Exception:
        return False
    return False


def hasConfigItem(someSection='Options', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):
    try:
        import ConfigParser as configparser
    except Exception:
        import configparser
    config = configparser.ConfigParser()
    try:
        config.read(thePath)
        return config.has_option(someSection, theInputKey)
    except Exception:
        return False
    return False


def extractBlackList(someSourceFile):
    tempfiledata = readFile(someSourceFile)
    return extractIPv4Addr(tempfiledata)


def handleBlackListURL(someURL, temp_dir):
    import os
    cachefile = os.path.join(temp_dir, "blacklist_download.tmp")
    getBlackList(someURL, cachefile)
    return extractBlackList(cachefile)


def compactList(someList, intern_func=None):
    if intern_func is None:
        def intern_func(x):
            return x
    seen = {}
    result = []
    for item in someList:
        marker = intern_func(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def printFlatIPBlacklistFile(manyIP):
    for ip in manyIP:
        print(str(ip))
    return None


def writeFlatIPBlacklistFile(manyIP, denyFile):
    first_text = False
    for ip in manyIP:
        if first_text is False:
            writeFile(denyFile, str(ip))
            first_text = True
        else:
            appendFile(denyFile, str(ip))
    return None


def generateIPDenyHostEntry(someIP, someService='ALL'):
    theResult = str(someService)
    theResult += str(': ')
    theResult += someIP
    return theResult


def printIPDenyHostEntry(someIP, someService='ALL'):
    print(str(generateIPDenyHostEntry(someIP, someService)))
    return None


def generateIPDenyHostFile(manyIP):
    manyEntry = [generateIPDenyHostEntry(ip) for ip in manyIP]
    return manyEntry


def printIPDenyHostFile(manyIP, someService='ALL'):
    for ip in manyIP:
        print(str(generateIPDenyHostEntry(ip, someService)))
    return None


def writeIPDenyHostFile(manyIP, someService='ALL', denyFile='/etc/hosts.deny'):
    for ip in manyIP:
        appendFile(denyFile, generateIPDenyHostEntry(ip, someService))
    return None


def printSnortIPBlacklistFile(manyIP):
    for ip in manyIP:
        print(str(ip))
    return None


def writeSnortIPBlacklistFile(manyIP, denyFile='/etc/snort/rules/black_list.rules'):
    first_text = False
    for ip in manyIP:
        if first_text is False:
            writeFile(denyFile, str(ip))
            first_text = True
        else:
            appendFile(denyFile, str(ip))
    return None


def generateIPDenySplunkEntry(someIP):
    theResult = str('acceptFrom = !' + str(someIP))
    theResult += str('\n')
    return theResult


def printIPDenySplunkEntry(someIP):
    print(str(generateIPDenySplunkEntry(someIP)))
    return None


def printSplunkIPBlacklistFile(manyIP):
    for ip in manyIP:
        print(str(generateIPDenySplunkEntry(ip)))
    return None


# EXPERIMENTAL
def writeSplunkIPBlacklistFile(manyIP, denyFile='/opt/splunk/etc/system/local/inputs.conf'):
    for ip in manyIP:
        appendFile(denyFile, str(generateIPDenySplunkEntry(ip)))
    return None


def generateIPDenyNginxEntryLine(someIP):
    theResult = str('deny ')
    theResult += someIP
    theResult += str(';\n')
    return theResult


def generateIPDenyNginxEntry(someIP, someLocation='/'):
    theResult = str("location ")
    theResult += str(someLocation)
    theResult += str('{\n\tdeny ')
    theResult += someIP
    theResult += str(';\n} ')
    return theResult


def printIPDenyNginxEntry(someIP, someLocation='/'):
    print(str(generateIPDenyNginxEntry(someIP, someLocation)))
    return None


# EXPERIMENTAL
def printNginxIPBlacklistFile(manyIP, someLocation='/'):
    theNginxResult = str("location ")
    theNginxResult += str(someLocation)
    theNginxResult += str('{\n')
    for ip in manyIP:
        theNginxResult += generateIPDenyNginxEntryLine(ip)
    theNginxResult += str('\n} ')
    print(str(theNginxResult))
    return None


# EXPERIMENTAL
def writeNginxIPBlacklistFile(manyIP, someLocation='/', denyFile='/etc/nginx/conf/raw_blacklist.conf'):  # noqa E501
    theNginxResult = str("location ")
    theNginxResult += str(someLocation)
    theNginxResult += str('{\n')
    for ip in manyIP:
        theNginxResult += generateIPDenyNginxEntryLine(ip)
    theNginxResult += str('\n} ')
    writeFile(denyFile, str(theNginxResult))
    return None


# iptables
def generateIPTablesDenyEntry(someIP, someChain='INPUT', someTarget='DROP'):
    theResult = str('-A ')
    theResult += str(someChain)
    theResult += str(' -s ')
    theResult += str(someIP)
    theResult += str(' -j ')
    theResult += str(someTarget)
    return theResult


def printIPTablesDenyEntry(someIP, someChain='INPUT', someTarget='DROP'):
    print(str(generateIPTablesDenyEntry(someIP, someChain, someTarget)))
    return None


def generateIPTablesDenyFile(manyIP):
    manyEntry = [generateIPTablesDenyEntry(ip) for ip in manyIP]
    return manyEntry


def printIPTablesDenyFile(manyIP, someChain='INPUT', someTarget='DROP', printHeaders=False):
    if printHeaders:
        print(str('*filter\n'))
        print(str(':'))
        print(str(someChain))
        print(str(' - [0:0]'))
    for ip in manyIP:
        print(str(generateIPTablesDenyEntry(ip, someChain, someTarget)))
    if printHeaders:
        print(str('COMMIT'))
        print(str(''))
    return None


def writeIPTablesDenyFile(manyIP, denyFile='/etc/blacklist.rules', someChain='INPUT', someTarget="DROP", printHeaders=False):  # noqa E501
    first_text = True
    if printHeaders:
        writeFile(denyFile, '*filter\n:')
        appendFile(denyFile, str(someChain))
        appendFile(denyFile, ' - [0:0]')
        first_text = False
    for ip in manyIP:
        if first_text is False:
            writeFile(denyFile, generateIPTablesDenyEntry(ip, someChain, someTarget))
            first_text = True
        else:
            appendFile(denyFile, generateIPTablesDenyEntry(ip, someChain, someTarget))
    if printHeaders:
        appendFile(denyFile, 'COMMIT')
    print(str(''))
    return None


# PF Firewall rules
# Caveat: manually adding the IPs to an ip set and then writing one rule for the set is
# significantly more efficient
def generatePFDenyEntry(someIP, someDirection='in', useQuick=True):
    theResult = str('block ')
    theResult += str(someDirection)
    theResult += str(' ')
    if useQuick is True:
        theResult += str('quick ')
    theResult += str('from ')
    theResult += str(someIP)
    return theResult


def printPFDenyEntry(someIP, someDirection='in', useQuick=True):
    print(str(generatePFDenyEntry(someIP, someDirection, useQuick)))
    return None


def generatePFDenyFile(manyIP, someDirection='in', useQuick=True):
    manyEntry = [generatePFDenyEntry(ip, someDirection, useQuick) for ip in manyIP]
    return manyEntry


def printPFDenyFile(manyIP, someDirection='in', useQuick=True, printHeaders=False):
    if printHeaders:
        print(str(
            '# Caveat: manually adding the IPs to an ip set and then writing one' +
            'rule for the set is significantly more efficient\n'
        ))
        print(str('\n'))
    for ip in manyIP:
        print(str(generatePFDenyEntry(ip, someDirection, useQuick)))
    return None


def writePFDenyFile(manyIP, someDirection='in', useQuick=True, denyFile='/etc/blacklist_pf.conf'):
    first_text = True
    for ip in manyIP:
        if first_text is False:
            writeFile(denyFile, generatePFDenyEntry(ip, someDirection, useQuick))
            first_text = True
        else:
            appendFile(denyFile, generatePFDenyEntry(ip, someDirection, useQuick))
    return None


def printEximIPBlacklistFile(manyIP):
    for ip in manyIP:
        print(str(ip))
    return None


def writeEximIPBlacklistFile(manyIP, denyFile='/etc/exim4/local_host_blacklist'):
    first_text = False
    for ip in manyIP:
        if first_text is False:
            writeFile(denyFile, str(ip))
            first_text = True
        else:
            appendFile(denyFile, str(ip))
    return None


def main():
    args = parseArgs()
    if args.dry_run is True:
        print(str("Fetch Public Blacklists: dry run"))
    if args.config is not None:
        tmp_dir = "/tmp/"
        try:
            temp_url_list = extractConfigItem('URL Sources', 'urls', args.config).split(",")
        except Exception:
            if (args.dry_run is False):
                print(str("Fetch Public Blacklists: Error: No Configuration File"))
                exit(3)
            else:
                print(str("Fetch Public Blacklists: Dry Run: Improvising Configuration"))
                temp_url_list = ['http://www.nothink.org/blacklist/blacklist_ssh_day.txt']

        if hasConfigItem('Options', 'hosts_deny_enabled', args.config) is True:
            active_hosts_deny = extractConfigBool('Options', 'hosts_deny_enabled', args.config)
            if hasConfigItem('Options', 'hosts_deny_append', args.config) is True:
                append_hosts_deny_file = extractConfigBool(
                    'Options',
                    'hosts_deny_append',
                    args.config
                )
            else:
                append_hosts_deny_file = False
            if hasConfigItem('Options', 'hosts_deny_file', args.config) is True:
                active_hosts_file = extractConfigItem('Options', 'hosts_deny_file', args.config)
            else:
                active_hosts_file = '/etc/hosts.deny'
        else:
            active_hosts_deny = args.hosts_deny

        if hasConfigItem('Options', 'snort_deny_enabled', args.config) is True:
            active_snort_deny = extractConfigBool('Options', 'snort_deny_enabled', args.config)
            if hasConfigItem('Options', 'snort_deny_file', args.config) is True:
                active_snort_file = extractConfigItem('Options', 'snort_deny_file', args.config)
            else:
                active_snort_file = args.snort_blacklist
        else:
            active_snort_deny = args.snort_deny

        if hasConfigItem('Options', 'nginx_deny_enabled', args.config) is True:
            active_nginx_deny = extractConfigBool('Options', 'nginx_deny_enabled', args.config)
            if hasConfigItem('Options', 'nginx_deny_file', args.config) is True:
                active_nginx_file = extractConfigItem('Options', 'nginx_deny_file', args.config)
            else:
                active_nginx_file = args.nginx_blacklist
        else:
            active_nginx_deny = args.nginx_deny

        if hasConfigItem('Options', 'splunk_deny_enabled', args.config) is True:
            active_splunk_deny = extractConfigBool('Options', 'splunk_deny_enabled', args.config)
            if hasConfigItem('Options', 'splunk_splunk_file', args.config) is True:
                active_splunk_file = extractConfigItem('Options', 'splunk_deny_file', args.config)
            else:
                active_splunk_file = args.splunk_blacklist
        else:
            active_splunk_deny = args.splunk_deny

        if hasConfigItem('Options', 'iptables_deny_enabled', args.config) is True:
            active_iptables_deny = extractConfigBool(
                'Options',
                'iptables_deny_enabled',
                args.config
            )
            if hasConfigItem('Options', 'iptables_deny_file', args.config) is True:
                active_iptables_file = extractConfigItem(
                    'Options',
                    'iptables_deny_file',
                    args.config
                )
            else:
                active_iptables_file = args.iptables_blacklist
        else:
            active_iptables_deny = args.iptables_deny

        if hasConfigItem('Options', 'pf_deny_enabled', args.config) is True:
            active_pf_deny = extractConfigBool('Options', 'pf_deny_enabled', args.config)
            if hasConfigItem('Options', 'pf_deny_file', args.config) is True:
                active_pf_file = extractConfigItem('Options', 'pf_deny_file', args.config)
            else:
                active_pf_file = args.pf_blacklist
        else:
            active_pf_deny = args.pf_deny

        if hasConfigItem('Options', 'exim4_deny_enabled', args.config) is True:
            active_exim4_deny = extractConfigBool('Options', 'exim4_deny_enabled', args.config)
            if hasConfigItem('Options', 'exim4_deny_file', args.config) is True:
                active_exim4_file = extractConfigItem('Options', 'exim4_deny_file', args.config)
            else:
                active_exim4_file = args.exim4_deny
        else:
            active_exim4_deny = args.exim4_deny

        temp_list = None
        for nURL in temp_url_list:
            if args.display is True:
                print(str("now on "))
                print(str("URL "), nURL)
            if temp_list is None:
                temp_list = handleBlackListURL(nURL, tmp_dir)
            else:
                temp_list += handleBlackListURL(nURL, tmp_dir)
            temp_list = helpers.compress_ip_list_to_cidr(compactList(temp_list))
        if args.display is True:
            if active_hosts_deny is True:
                print(str('#'))
                print(str('# /etc/hosts.deny file'))
                print(str('#'))
                printIPDenyHostFile(temp_list, 'ALL')
                print(str(''))
            if active_snort_deny is True:
                print(str('#'))
                print(str('# snort blacklist file'))
                print(str('#'))
                printSnortIPBlacklistFile(temp_list)
                print(str(''))
            if active_nginx_deny is True:
                print(str('#'))
                print(str('# nginx blacklist file'))
                print(str('#'))
                printNginxIPBlacklistFile(temp_list)
                print(str(''))
            if active_splunk_deny is True:
                print(str('#'))
                print(str('# Splunk blacklist file'))
                print(str('#'))
                printSplunkIPBlacklistFile(temp_list)
                print(str(''))
            if active_iptables_deny is True:
                print(str('#'))
                print(str('# iptables-restore blacklist rules file'))
                print(str('#'))
                printIPTablesDenyFile(temp_list)
                print(str(''))
            if active_pf_deny is True:
                print(str('#'))
                print(str('# pf firewall blacklist rules config file'))
                print(str('#'))
                printPFDenyFile(temp_list)
                print(str(''))
            if active_exim4_deny is True:
                print(str('#'))
                print(str('# exim4 blacklist file'))
                print(str('#'))
                printEximIPBlacklistFile(temp_list)
                print(str(''))
        if args.dry_run is False:
            if active_hosts_deny is True:
                writeIPDenyHostFile(temp_list, 'ALL', active_hosts_file)
            if append_hosts_deny_file is True:
                writeIPDenyHostFile(temp_list, 'ALL', '/etc/hosts.deny')
            if active_snort_deny is True:
                writeSnortIPBlacklistFile(temp_list, active_snort_file)
            if active_nginx_deny is True:
                writeNginxIPBlacklistFile(temp_list, active_nginx_file)
            if active_splunk_deny is True:
                writeSplunkIPBlacklistFile(temp_list, active_splunk_file)
            if active_iptables_deny is True:
                writeIPTablesDenyFile(temp_list, active_iptables_file)
            if active_pf_deny is True:
                writePFDenyFile(temp_list, active_pf_file)
            if active_exim4_deny is True:
                writeEximIPBlacklistFile(temp_list, active_exim4_file)
            print(str(temp_list))
    else:
        print(str("nothing to do"))

    exit(0)


if __name__ == '__main__':
    main()
