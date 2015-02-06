#coding=utf-8
__author__ = 'Administrator'

import simplejson
def ReadProperties(pFileName):
    f=open(pFileName)
    d=simplejson.load(f)
    f.close()
    return d
