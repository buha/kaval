#!/usr/bin/python3

def isinteger(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def isfloat(n):
    return isinstance(n, float)


