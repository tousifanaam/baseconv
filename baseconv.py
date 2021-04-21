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
        return None
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
        number = chunk(list(str(number)), 4)
        l = [8, 4, 2, 1]
        hexex = [
            'A', 'B', 'C', 
            'D', 'E', 'F']
        res = ""
        for i in number:
            count = 0
            for n in range(len(l)):
                if i[n] == '1':
                    count += l[n]
                elif i[n] != "0":
                    return None
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

def ip_to_cidr_sub(ip, subnet):
    subnet = [decbin(i) for i in subnet.split('.')]
    n = 0
    for i in subnet:
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

def subnet(cidr: str, details: bool = False):
    """
    >>> subnet('192.168.0.1/16')
    '192.168.0.0'
    """
    # no argument validation in place atm
    # invalid argument will result in
    # incorrect results
    ip, subnet = (cidr[:-3], cidr[-2:].lstrip('/'))
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
    if details:
        res = {'subnet':res}
        res['subnet_mask'] = '.'.join(map(lambda x: str(bindec(x)),[pre_bin[:8], pre_bin[8:16], pre_bin[16:24], pre_bin[24:32]]))
        net, host = ip_bin[:pre_bin.count('1')], ip_bin[pre_bin.count('1'):]
        res['first_host'] = '.'.join(res['subnet'].split('.')[:3]) + '.' + str(int(res['subnet'].split('.')[3]) + 1)
        a = net + '1'*(len(host) - 1) + '0'
        res['last_host'] = '.'.join(tuple(map(lambda x: str(bindec(x)), [a[:8], a[8:16], a[16:24], a[24:32]])))
        a = net + '1'*(len(host))
        res['broadcast'] = '.'.join(tuple(map(lambda x: str(bindec(x)), [a[:8], a[8:16], a[16:24], a[24:32]])))
    return res

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
        print("ERR: argument missing", end='')