# encoding: utf-8

import string
import random


__all__ = ['randpass']



def randpass(minlength=5, maxlength=25, pool=string.ascii_letters + string.digits):
    length = random.randint(minlength,maxlength)
    return ''.join([random.choice(pool) for _ in range(length)])
