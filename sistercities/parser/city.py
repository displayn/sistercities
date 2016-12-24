# -*- coding: utf-8 -*-
class City(object):
    def __init__(self, name, revid, queryrunid, source):
        self.name = name
        self.revid = revid
        self.queryrunid = queryrunid
        self.source = source

    def getName(self):
        return self.name

    def isValid(self):
        request = True
        if (request):
            return True
        return False
