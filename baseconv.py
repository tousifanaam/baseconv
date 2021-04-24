#!/usr/bin/env python3

__author__ = "Tousif Anaam"
__version__ = '$Revision: 0.2 $'
__source__ = 'https://github.com/tousifanaam/baseconv'


def bindec(number, style=False):
    """
    binary to decimal
    >>> bindec(11111111)
    255
    """
    number = list(str(number)[::-1])
    res = 0
    for i in range(len(number)):
        if number[i] == '1':
            d = 2 ** i
            res += d
        elif number[i] != '0':
            raise ValueError("({0}) '{1}' - not a valid binary number.".format(number[i], "".join(number)))
    if len(str(res)) == 3 and style == True:
        res = str(res)
        style = False
    _flag = False
    if len(str(res)) != 3 and len(str(res)) % 3 == 0 and style == True:
        _flag = True
    if style == True:
        res = str(res)[::-1]
        n_res = ""
        n = 0
        for i in res:
            n_res += i
            n += 1
            if n == 3:
                n_res += ","
                n = 0
        res = n_res[::-1].lstrip(" ")
        if _flag == True:
            res = res.lstrip(",")
    return res

def decbin(number, style=False):
    """
    decimal to binary
    >>> decbin(255)
    '11111111'
    """
    try:
        number = int(number)
    except ValueError:
        raise ValueError('{0} - invalid base 10 integer.'.format(number))
    ons = []
    for i in range(0,number):
        bit = 2 ** i
        if bit > number:
            break
        else:
            ons.append(bit)
    ons = ons[::-1]
    res = ''
    for i in ons:
        if i <= number:
            number -= i
            res += '1'
        elif i > number:
            res += '0'
    if style == True:
        res = res[::-1]
        n_res = ""
        n = 0
        for i in res:
            n_res += i
            n += 1
            if n == 4:
                n_res += " "
                n = 0
        if n != 0:
            while n < 4:
                n_res += "0"
                n += 1
        res = n_res[::-1].lstrip(" ")
    return res

def hexbin(number, style=False):
    """
    hexadecimal to binary
    >>> hexbin('F2')
    '11110010'
    """
    l = [8, 4, 2, 1]
    number = list(str(number).upper())
    strings = [
        '0', '1', '2', '3', '4', 
        '5', '6', '7', '8', '9']
    extrastrings = [
        'A', 'B', 'C', 
        'D', 'E', 'F']
    res = ""
    for i in number:
        if i in strings:
            v = int(i)
            for n in l:
                if n <= v:
                    res += "1"
                    v -= n
                else:
                    res += "0"
        elif i in extrastrings:
            v = 10 + extrastrings.index(i)
            for n in l:
                if n <= v:
                    res += "1"
                    v -= n
                else:
                    res += "0"
        else:
            raise ValueError("({0}) '{1}' - not a valid hexadecimal number.".format(i, "".join(number)))
    if style == True:
        res = res[::-1]
        n_res = ""
        n = 0
        for i in res:
            n_res += i
            n += 1
            if n == 4:
                n_res += " "
                n = 0
        if n != 0:
            while n < 4:
                n_res += "0"
                n += 1
        res = n_res[::-1].lstrip(" ")
    return res

def binhex(number, style=False):
    """
    binary to hexadecimal
    >>> binhex(1111)
    'F'
    """
    def chunk(a, n: int):
        return [a[i: i + n] for i in range(0, len(a), n)]

    if len(str(number)) % 4 == 0:
        x, number = number, chunk(list(str(number)), 4)
        l = [8, 4, 2, 1]
        hexex = ['A', 'B', 'C', 'D', 'E', 'F']
        res = ""
        for i in number:
            count = 0
            for n in range(len(l)):
                if i[n] == '1':
                    count += l[n]
                elif i[n] != "0":
                    raise ValueError("({0}) '{1}' - invalid binary number.".format(i[n], x))
            if count <= 9:
                res += str(count)
            else:
                index = (count - 10)
                res += hexex[index]
        if len(str(res)) == 4 and style == True:
            res = str(res)
            style = False
        if style == True:
            res = res[::-1]
            n_res = ""
            n = 0
            for i in res:
                n_res += i
                n += 1
                if n == 4:
                    n_res += " "
                    n = 0
            res = n_res[::-1].lstrip(" ")
    else:
        r = len(str(number)) % 4
        new = ""
        for i in range(r):
            new += "0"
        new += number
        if style == True:
            return binhex(new, True)
        else:
            return binhex(new)
    return res

def dechex(number, style=False):
    """
    >>> dechex('4095')
    'FFF'
    """
    return binhex(decbin(number), style)

def hexdec(number, style=False):
    """
    >>> hexdec('FFF')
    4095
    """
    return bindec(hexbin(number), style)

def binary_addition(nums: tuple, style=False) -> str:
    """add binary numbers"""
    return decbin(sum(map(lambda x: bindec(x), nums)), style)

def hex_addition(nums: tuple, style=False):
    """hexadecimal addition"""
    return binhex(decbin(sum(map(lambda x: bindec(hexbin(x)), nums))), style)

def _foo():
    "generator func for all ipv4 address"
    for a in range(1,256):
        for b in range (1,256):
            for c in range(1,256):
                for d in range(1,256):
                    yield '{0}.{1}.{2}.{3}'.format(a, b, c, d)

def _check_class(ip: str) -> int:
    """
    Pre CIDR IPv4 Class
    0 -> Class A
    1 -> Class B
    2 -> Class C
    3 -> Class D
    4 -> Class E
    """
    check = decbin(ip.split('.')[0])
    if check == None:
        check = '0' * 8
    elif len(check) < 8:
        check = '0' * (8 - len(check)) + check
    if check.startswith('0'):
        return 0
    elif check.startswith('10'):
        return 1
    elif check.startswith('110'):
        return 2
    elif check.startswith('1110'):
        return 3
    elif check.startswith('1111'):
        return 4

def ip_to_cidr(ip, mask):
    """
    >>> ip_to_cidr('192.168.0.1', '255.255.255.0')
    '192.168.0.1/24'
    """
    mask = [decbin(i) for i in mask.split('.')]
    n = 0
    for i in mask:
        if '0' not in i:
            n += len(i)
        else:
            for x in i:
                if x == '1':
                    n += 1
                else:
                    break
            break
    return ip + "/{0}".format(n)


wildcards = {'32': '255.255.255.255', '31': '255.255.255.254', '30': '255.255.255.252', 
            '29': '255.255.255.248', '28': '255.255.255.240', '27': '255.255.255.224', 
            '26': '255.255.255.192', '25': '255.255.255.128', '24': '255.255.255.0', 
            '23': '255.255.254.0', '22': '255.255.252.0', '21': '255.255.248.0', 
            '20': '255.255.240.0', '19': '255.255.224.0', '18': '255.255.192.0',
            '17': '255.255.128.0', '16': '255.255.0.0', '15': '255.254.0.0', 
            '14': '255.252.0.0', '13': '255.248.0.0', '12': '255.240.0.0', 
            '11': '255.224.0.0', '10': '255.192.0.0', '9': '255.128.0.0', 
            '8': '255.0.0.0', '7': '254.0.0.0', '6': '252.0.0.0', 
            '5': '248.0.0.0', '4': '240.0.0.0', '3': '224.0.0.0', 
            '2': '192.0.0.0', '1': '128.0.0.0', '0': '0.0.0.0',}

def subnet(cidr: str, details: bool = False, more_details: bool = False):
    """
    >>> subnet('192.168.0.1/16')
    '192.168.0.0'
    """
    # no argument validation in place atm
    # invalid argument will result in
    # incorrect results
    ip, subnet = (cidr[:-2].rstrip('/'), cidr[-2:].lstrip('/'))
    ip_bin = list(map(lambda x: decbin(x), ip.split('.')))
    for n, i in enumerate(ip_bin):
        x = i
        if i == None:
            x = '0' * 8
        elif len(i) < 8:
            x = '0' * (8 - len(i)) + i
        ip_bin[n] = x
    pre_bin = "1"*int(subnet) + "0"*(32 - int(subnet))
    ip_bin = "".join(ip_bin)
    load = tuple(zip(ip_bin, pre_bin))
    sub = ''
    for i in load:
        if i[1] == '1':
            sub += i[0]
        else:
            break
    sub = sub + '0'*(32 - len(sub))
    sub =  [sub[:8], sub[8:16], sub[16:24], sub[24:32]]
    res = '.'.join(tuple(map(lambda x: str(bindec(x)), sub)))
    if details or more_details:
        res = {'subnet':res}
        res['cidr'] = cidr
        res['subnet_mask'] = '.'.join(map(lambda x: str(bindec(x)),[pre_bin[:8], pre_bin[8:16], pre_bin[16:24], pre_bin[24:32]]))
        net, host = ip_bin[:pre_bin.count('1')], ip_bin[pre_bin.count('1'):]
        res['subnet_mask_cidr'] = int(res['cidr'][-2:].lstrip('/'))
        res['first_host'] = '.'.join(res['subnet'].split('.')[:3]) + '.' + str(int(res['subnet'].split('.')[3]) + 1)
        a = net + '1'*(len(host) - 1) + '0'
        res['last_host'] = '.'.join(tuple(map(lambda x: str(bindec(x)), [a[:8], a[8:16], a[16:24], a[24:32]])))
        res['host_count'] = (2 ** len(host)) - 2
        res['net_count'] = (2 ** len(host))
        a = net + '1'*(len(host))
        res['broadcast'] = '.'.join(tuple(map(lambda x: str(bindec(x)), [a[:8], a[8:16], a[16:24], a[24:32]])))
        res['wildcard'] = [v for k,v in wildcards.items() if k == str(res['subnet_mask_cidr'])][0]
        if more_details:
            res['_extra'] = {}
            extra = res['_extra']
            extra['mask_bin_string_no_dot'] = pre_bin
            extra['subnet_bin_string_no_dot'] = ip_bin
            extra['subnet_net_portion_bin_string_no_dot'] = net
            extra['subnet_host_portion_bin_string_no_dot'] = host
    return res

def _log(number: int, base: int = 2):
	# base ^ x = number <-- x is answer
    # explicit condition for only this case
    for i in range(1, 33):
        trial = base ** i
        if trial == number:
            return i
    else:
        raise ValueError('Failed to solve log_{0}({1})'.format(base, number))

def divide_subnet_per_host(cidr: str, hostcount: int = None, only_cidr: bool = False, details: bool = False, more_details: bool = False, full_details: bool = False):
    """ + _ + """
    data = subnet(cidr, more_details=True)
    for i in range(data['subnet_mask_cidr'] + 1, 31):
        if subnet("{0}/{1}".format(data['subnet'], i), details=True)['host_count'] == hostcount:
            new_mask = subnet("{0}/{1}".format(data['subnet'], i), details=True)['subnet_mask']
    cidr2 = ip_to_cidr(data['subnet'], new_mask)
    if only_cidr:
        return cidr2
    n = _log(hostcount + 2)
    def _divide_subnet(cidr1, cidr2):
        data1 = subnet(cidr1, more_details=True)
        data2 = subnet(cidr2, more_details=True)
        s = '0' * n
        results = []
        for _ in range(data2['net_count']):
            new = data1['_extra']['subnet_net_portion_bin_string_no_dot']+ s + data2['_extra']['subnet_host_portion_bin_string_no_dot']
            res = '.'.join(map(lambda x: str(bindec(x)),[new[:8], new[8:16], new[16:24], new[24:32]])) + '/' + cidr2[-2:].lstrip('/')
            results.append(res)
            s = binary_addition((s, '1'))
            if len(s) < n:
                s = '0'*(n - len(s)) + s
        if details or more_details or full_details:
            results = {'_all': results}
            results['parent_subnet'] = cidr1
            results['first_network'] = results['_all'][0]
            results['last_network'] = results['_all'][-1]
            results['subnet_mask'] = new_mask
            results['subnet_mask_cidr'] = data2['subnet_mask_cidr']
            results['host_count_per_net'] = len(results['_all']) - 2
            results['net_count'] = len(results['_all'])
            if more_details or full_details:
                results['_all'] = [subnet(i, details=True) for i in results['_all']]
                if full_details:
                    results['_all'] = [subnet(i['cidr'], more_details=True) for i in results['_all']]
        return results
    return _divide_subnet(data['cidr'], cidr2)

def divide_subnet_per_net(cidr: str, netcount: int, only_cidr: bool = False, details: bool = False, more_details: bool = False, full_details: bool = False):
    data = subnet(cidr, more_details=True)
    v = netcount
    while True:
        try:
            _log(v)
            break
        except ValueError:
            v += 1
    x1 = data['_extra']['mask_bin_string_no_dot'].count('1')
    for i in range(data['subnet_mask_cidr'] + 1, 33):
        if data['net_count'] / subnet(f"{data['subnet']}/{i}", details=True)['net_count'] == v:
            r = subnet(f"{data['subnet']}/{i}", more_details=True)
            sub_cidr = r['subnet_mask_cidr']
            sub_mask = r['subnet_mask']
            x2 = r['_extra']['mask_bin_string_no_dot'].count('1')
    if only_cidr:
        return r['cidr']
    change_index = x2 - x1
    s = '0' * change_index
    results = []
    while True:
        b = "{0}".format(data['_extra']['subnet_net_portion_bin_string_no_dot']) + s + r['_extra']['subnet_host_portion_bin_string_no_dot']
        res = '.'.join(map(lambda x: str(bindec(x)),[b[:8], b[8:16], b[16:24], b[24:32]])) + '/' + str(sub_cidr)
        results.append(res)
        s = binary_addition((s, '1'))
        if len(s) < change_index:
            s = '0'*(change_index - len(s)) + s
        if s == '1' * change_index:
            b = "{0}".format(data['_extra']['subnet_net_portion_bin_string_no_dot']) + s + r['_extra']['subnet_host_portion_bin_string_no_dot']
            res = '.'.join(map(lambda x: str(bindec(x)),[b[:8], b[8:16], b[16:24], b[24:32]])) + '/' + str(sub_cidr)
            results.append(res)
            break
    if details or more_details or full_details:
        results = {'_all': results}
        results['parent_subnet'] = data['subnet'] + '/' + str(data['subnet_mask_cidr'])
        results['first_network'] = results['_all'][0]
        results['last_network'] = results['_all'][-1]
        results['subnet_mask'] = sub_mask
        results['subnet_mask_cidr'] = sub_cidr
        if more_details or full_details:
            results['_all'] = [subnet(i, details=True) for i in results['_all']]
            if full_details:
                results['_all'] = [subnet(i['cidr'], more_details=True) for i in results['_all']]
    return results

def cidr_to_netmask(cidr):
    """
    >>> cidr_to_netmask('208.130.28.0/22')
    ('208.130.28.0', '255.255.252.0')
    """
    return subnet(cidr, True)['subnet'], subnet(cidr, True)['subnet_mask']

def cidr_verbose(cidr: str):
    """
    Really elegant code! Using the builtin
    ipaddress module.

    inspired source: https://gist.github.com/vndmtrx/dc412e4d8481053ddef85c678f3323a6#gistcomment-3237804
    """
    import ipaddress

    ipi = ipaddress.ip_interface(cidr)
    print("Address:   ", ipi.ip)
    print("Mask:      ", ipi.netmask)
    print("Cidr:      ", str(ipi.network).split('/')[1])
    print("Network:   ", str(ipi.network).split('/')[0])
    print("Broadcast: ", ipi.network.broadcast_address)
    
def main(base):
    """
    --- main func ---
    [-b] or [2] prompt to provide a binary number
    [-d] or [10] prompt to provide decimal number
    [-h] or [16] promt to provide hexadecimal number
    """
    if base == 10 or base == "10" or base == "-d":
        x = input("DEC:  ")
        print("BIN:  " + decbin(x, True))
        print("HEX:  " + binhex(decbin(x), True))
    elif base == 2 or base == "2" or base == "-b":
        x = input("BIN:  ")
        print("DEC:  " + bindec(x, True))
        print("HEX:  " + binhex(x, True))
    elif base == 16 or base == "16" or base == "-h":
        x = input("HEX:  ")
        print("BIN:  " + hexbin(x, True))
        print("DEC:  " + bindec(hexbin(x), True))
    else:
        raise ValueError("Base %s is not available." % base)

if __name__ == '__main__':
    import sys
    try:
        main(sys.argv[1])
    except IndexError:
        print("usage: baseconv.py [-b] or [-h] or [-d]")
        print("ERR: argument missing")
