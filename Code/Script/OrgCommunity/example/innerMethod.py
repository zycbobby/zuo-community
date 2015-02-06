#coding=utf-8
__author__ = 'Administrator'

class Person(object):
    def __init__(self,name):
        self.name=name

    def __showname(self):
        print self.name

    def showname(self):
        print self.name
if __name__=='__main__':
    t=Person('zuo')
    t.__showname()#wrong
    t._Person__showname()#correct
    t.showname()#correct