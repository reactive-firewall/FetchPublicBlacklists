#! /usr/bin/env python


# IP string conversion 00000000000000000000000000000000 <-> 0.0.0.0


DEFAULT_IPV4 = "0.0.0.0"


DEFAULT_IP = "00000000000000000000000000000000"


CIDR_LEN_VALUES = [
    2147483648, 1073741824, 536870912, 268435456, 134217728,
    67108864, 33554432, 16777216, 8388608, 4194304,
    2097152, 1048576, 524288, 262144, 131072,
    65536, 32768, 16384, 8192, 4096,
    2048, 1024, 512, 256, 128,
    64, 32, 16, 8, 4,
    2, 1
]


def IPv4_to_IP(someIPv4=DEFAULT_IPV4):
    temp_num = ""
    for octet in str(someIPv4).split("."):
        temp_num += "{0:08b}".format(int(octet))
    return temp_num


def IP_to_IPv4(someIP="00000000000000000000000000000000"):
    theResult = str(int(someIP[0:8], 2))
    theResult = theResult + "." + str(int(someIP[8:16], 2))
    theResult = theResult + "." + str(int(someIP[16:24], 2))
    theResult = theResult + "." + str(int(someIP[24:32], 2))
    return theResult


# IP int conversion 0 <-> 00000000000000000000000000000000b <-> 0.0.0.0


def int_to_IP(someInt="0"):
    theResult = str("{0:032}".format(int("{0:032b}".format(int(someInt)), 10)))
    return theResult


def int_to_IPv4(someInt="0"):
    return IP_to_IPv4(int_to_IP(someInt))


def IPv4_to_int(someIP=DEFAULT_IPV4):
    temp_num = ""
    if someIP is None:
        the_result = None
    else:
        for octet in someIP.split("."):
            temp_num += "{0:08b}".format(int(octet))
        the_result = int(temp_num, 2)
    return the_result


def IP_to_int(someIP="00000000000000000000000000000000"):
    theResult = int(someIP, 2)
    return theResult


# array conversions [00000000000000000000000000000000] <-> [0.0.0.0]


def IPv4s_to_IPs(someIPs=None):
    if someIPs is None:
        someIPs = [DEFAULT_IPV4]
    the_list = [IPv4_to_IP(someIP) for someIP in someIPs]
    return the_list


def IPs_to_IPv4s(someIPs=None):
    if someIPs is None:
        someIPs = [DEFAULT_IP]
    the_list = [IP_to_IPv4(someIP) for someIP in someIPs]
    return the_list


def IPv4s_to_ints(someIPs=None):
    if someIPs is None:
        someIPs = [DEFAULT_IPV4]
    the_list = [IPv4_to_int(someIP) for someIP in someIPs]
    return the_list


def IPs_to_ints(someIPs=None):
    if someIPs is None:
        someIPs = [DEFAULT_IP]
    the_list = [IP_to_int(someIP) for someIP in someIPs]
    return the_list


def ints_to_IPs(someInts=None):
    if someInts is None:
        someInts = [str("0")]
    the_list = [int_to_IP(someInt) for someInt in someInts]
    return the_list


def ints_to_IPv4s(someInts=None):
    if someInts is None:
        someInts = [str("0")]
    the_list = [int_to_IPv4(someInt) for someInt in someInts]
    return the_list


# useful utilities to find subnets and CIDR approximations


def Extract_Runs(someArray, gap=1):
    run = []
    result = [run]
    next_item = None
    for item in someArray:
        if (item == next_item) or (next_item is None):
            run.append(item)
        else:
            run = [item]
            result.append(run)
        next_item = item + gap
    return result


def chunk_array_to_size(in_array, a_size):
    if a_size is None:
        a_size = 1
    a = in_array
    b = a_size
    out_array = [a[i:(i + b)] for i in range(0, len(a), b)]
    return out_array


def chunk_IP_array_to_subnets(some_ip_array):
    lastSize = None
    for i in CIDR_LEN_VALUES:
        if lastSize is None:
            lastSize = i
            continue
        if (len(some_ip_array) >= lastSize) is False:
            lastSize = i
            if (len(some_ip_array) >= i):
                chunked_array = chunk_array_to_size(some_ip_array, i)
    return chunked_array


def Extract_IPv4_Runs(someIPv4Array, gap=1):
    result_ints = Extract_Runs(IPv4s_to_ints(someIPv4Array), gap)
    x = [ints_to_IPv4s(i) for i in result_ints]
    the_result = [chunk_IP_array_to_subnets(k) for k in x]
    the_result_IPv4_runs = []
    for somenet in the_result:
        for somehost in somenet:
            the_result_IPv4_runs.append(somehost)
    return the_result_IPv4_runs


def Compile_IPv4_Runs(someMixedArray, gap=1):
    someIPv4Array_tmp = [CIDR_to_IPv4s(i) for i in someMixedArray]
    someIPv4Array = []
    for anet in someIPv4Array_tmp:
        for someIPv4host in anet:
            someIPv4Array.append(someIPv4host)
    n = Extract_Runs(IPv4s_to_ints(someIPv4Array), gap)
    k = [ints_to_IPv4s(m) for m in n]
    x = [chunk_IP_array_to_subnets(j) for j in k]
    the_result = []
    for anet in x:
        for somehost in anet:
            the_result.append(somehost)
    return the_result


def get_IP_bit(someIP=None, some_bit=None):
    if someIP is None:
        someIP = DEFAULT_IP
    if some_bit is None:
        some_bit = 0
    theResult = str(int(someIP[0:some_bit], 2))
    return theResult


def get_IPv4_bit(someIPv4=None, some_bit=None):
    if someIPv4 is None:
        someIPv4 = DEFAULT_IPV4
    if some_bit is None:
        some_bit = 0
    theResult = get_IP_bit(IPv4_to_IP(someIPv4), some_bit)
    return theResult


def IP_to_CIDR(someIP=None, some_mask_bit=None):
    if someIP is None:
        someIP = DEFAULT_IP
    if some_mask_bit is None:
        some_mask_bit = 0
    theResult = str(someIP)
    if some_mask_bit is not 32:
        theResult = str(
            someIP[0:int(some_mask_bit)]
        ) + "{0:032b}".format(int(0))[int(some_mask_bit):32]
    return str(IP_to_IPv4(theResult) + "/" + str(some_mask_bit))


def IPv4_to_CIDR(someIP=None, some_mask_bit=None):
    if someIP is None:
        someIP = DEFAULT_IPV4
    if some_mask_bit is None:
        some_mask_bit = 0
    theResult = IP_to_CIDR(IPv4_to_IP(someIP), some_mask_bit)
    return theResult


def CIDR_to_IPv4s(someCIDR='127.0.0.1/32'):
    """This will assume input 127.0.0.1 = 127.0.0.1/32
    and blindly return [127.0.0.1]"""
    if '/' in someCIDR:
        somebit = someCIDR.split('/')[1]
        baseHost = IPv4_to_int(someCIDR.split('/')[0])
        theResult = list(range(pow(2, (32 - int(somebit)))))
        theResult[0] = int_to_IPv4(baseHost)
        for some_index in range(pow(2, (32 - int(somebit)))):
            theResult[some_index] = int_to_IPv4(baseHost + some_index)
    else:
        theResult = [someCIDR]
    return theResult


def no_op():
    return None


def IPRange_to_CIDR(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
    match_bit = 32
    for somebit in range(1, 32):
        a = IPv4_to_CIDR(startIPv4, int(somebit))
        b = IPv4_to_CIDR(endIPv4, int(somebit))
        if a == b:
            match_bit = somebit
    subnet = IPv4_to_CIDR(startIPv4, match_bit)
    return subnet


def IPRange_to_valid_CIDR(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
    match_bit = 32
    for somebit in range(1, 32):
        a = IPv4_to_CIDR(startIPv4, int(somebit))
        b = IPv4_to_CIDR(endIPv4, int(somebit))
        if a == b:
            c = int(IPv4_to_int(endIPv4) - IPv4_to_int(startIPv4))
            if c == pow(2, (32 - int(somebit))):
                match_bit = somebit
    subnet = IPv4_to_CIDR(startIPv4, match_bit)
    return subnet


def IPRange_to_best_mask(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
    match_bit = 32
    for somebit in range(1, 32):
        a = IPv4_to_CIDR(startIPv4, int(somebit))
        b = IPv4_to_CIDR(endIPv4, int(somebit))
        if a == b:
            c = int(IPv4_to_int(endIPv4) - IPv4_to_int(startIPv4))
            if c == pow(2, (32 - int(somebit))):
                match_bit = somebit
    return match_bit


def IPRange_to_mask(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
    match_bit = 32
    for somebit in range(1, 32):
        a = IPv4_to_CIDR(startIPv4, int(somebit))
        b = IPv4_to_CIDR(endIPv4, int(somebit))
        if a == b:
            match_bit = somebit
    return match_bit


def getNetAddrforIPv4(startIPv4=DEFAULT_IPV4, net_mask_bit=32):
    theResult = IPv4_to_CIDR(startIPv4, int(net_mask_bit))
    offset = -1 - len(str(net_mask_bit))
    return theResult[0:offset]


def compress_ip_list_to_cidr(someIPList=None):
    if someIPList is None:
        someIPList = [DEFAULT_IPV4]
    temp_list = Compile_IPv4_Runs(someIPList)
    theResult = None
    for l in temp_list:
        someResult = None
        if (l is None or l is [] or len(l) is 1) is False:
            someResult = IPv4_to_CIDR(
                l[0],
                IPRange_to_mask(l[0], l[-1])
            )
            if someResult is None:
                someResult = [IPv4_to_CIDR(i, 32) for i in l]
            if theResult is None:
                theResult = [someResult]
            else:
                theResult.append(someResult)
        elif (l is None or l is []) is False:
            if theResult is None:
                theResult = l
            else:
                theResult.append(l[0])
    return theResult


# not implemented
def getBcastAddrforIPv4():
    no_op()
    return False


def extractRegexPattern(theInput_Str, theInputPattern):
    import re
    sourceStr = str(theInput_Str)
    prog = re.compile(theInputPattern)
    theList = prog.findall(sourceStr)
    return theList


def extractIPv4Addr(theInputStr):
    return extractRegexPattern(
        theInputStr,
        "(?:(?:[[:print:]]*){0,1}(?P<IP>(?:" +
        "(?:[0-9]{1,3}[\.]{1}){3}(?:[0-9]" +
        "{1,3}){1}){1})+(?:[[:print:]]*){0,1})+"
    )

