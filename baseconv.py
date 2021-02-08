#!/usr/bin/env python3
import json

__author__ = "Tousif Anaam"

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
            return None
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
    >>> hexbin(F2)
    '10100010'
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
            return None
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
    def chunk(arr, size):
        l = []
        for i in range(0, len(arr), size):
            l.append(arr[i:i+size])
        return l
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

def ipdecbinclass(ip):
    """old style ipv4 stuff"""
    filename = "octets.json"
    with open(filename) as f:
        octets = json.load(f)
    ip = ip.split(".")
    ipbin = octets[int(ip[0])] + "." + octets[int(ip[1])] + "." + octets[int(ip[2])] + "." + octets[int(ip[3])]
    classA = list(range(1,127))
    classB = list(range(128,192))
    classC = list(range(192,224))
    classD = list(range(224,240))
    classE = list(range(240,256))

    if int(ip[0]) in classA:
        classtype = "A (first 8 bits - network portion -- Unicast)"
    elif int(ip[0]) == 127:
        classtype = "A (_ -- Loopback)"
    elif int(ip[0]) == 0:
        classtype = "A (_ -- Reserved for Network)"
    elif int(ip[0]) == 169 and int(ip[1]) == 254:
        classtype = "B (first 16 bits - network portion -- Unicast -- Link Local)"
    elif int(ip[0]) in classB:
        classtype = "B (first 16 bits - network portion -- Unicast)"
    elif int(ip[0]) in classC:
        classtype = "C (first 24 bits - network portion -- Unicast)"
    elif int(ip[0]) in classD:
        classtype = "D (_ -- Multicast)"
    elif int(ip[0]) in classE:
        classtype = "E (_ -- Reserved for Broadcast)"
    return ipbin, classtype

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