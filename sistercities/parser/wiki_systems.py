from sistercities.venv.src.pywikibot import pywikibot
class Wiki(object):
    def __init__(self, wikiname, searchstring):
        self.wikiname = wikiname
        self.searchstring = searchstring

    def getWikiname(self):
        return self.wikiname

    def getSearchString(self):
        return self.searchstring

    def DataObjectExist(self):
        return False