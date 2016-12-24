# -*- coding: utf-8 -*-
from sistercities.parser.downloader import Downloader
from sistercities.venv.src.pywikibot import pywikibot

#read List + Wikisystem

#hold citylist:
    #query cityname
de_wikipedia = 'de'
system = 'wikipedia'
wikidata = 'wikidata'
list_url = 'Liste_der_Städte_in_Deutschland'

list_filter = [
            'Stadt',
            'Deutschland',
            'Gemeinde (Deutschland)',
            'Stadtrecht',
            'Land (Deutschland)',
            'Liste der flächengrößten Städte und Gemeinden Deutschlands',
            'Liste der Großstädte in Deutschland',
            'Liste der Groß- und Mittelstädte in Deutschland',
            'Agglomeration#Deutschland',
            'Liste der größten deutschen Städte',
            'Liste der kleinsten Städte in Deutschland nach Einwohnerzahl',
            'Liste der Städte in Brandenburg',
            'Liste der Städte in Mecklenburg-Vorpommern',
            'Liste der Städte in Thüringen',
            'Liste der Städte im Saarland',
            'Liste ehemaliger Städte in Deutschland',
            'Kategorie:Liste (Gemeinden in Deutschland)',
            'Kategorie:Liste (Städte nach Staat)'
            ]

section_keywords = [
                    'Städtepartnerschaften',
                    'Städtepartnerschaft',
                    'Schwesterstädte',
                    'Partnerstädte',
                    'Partnerschaften',
                    'Gemeindepartnerschaft'
                    ]


# get current Revision id from List
def getRevId(language, wikisystem, URL):
    wiki = pywikibot.getSite(language, wikisystem)
    revID = pywikibot.Page(wikisystem, URL)
    return str(revID)


# download file
def downloadFile(self, language, wikisystem, URL):
    wiki = pywikibot.Site(language, wikisystem)
    RevID = Downloader.getRevId(self.language, self.wikisystem, self.URL)
    try:
        text_file = open(RevID + '_list_' + self.language + '_cities.txt', 'w')
        text_file.write(pywikibot.Page(self.wiki, self.URL).text)
        text_file.close()
    except OSError:
        pass

        #check if wikidata object exist


        #find in wikitext_de
            #collect names
                #check if found city is a city
            #put only valid cities in list
        #query wikidata entry
            #getList for Property

