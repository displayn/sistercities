# -*- coding: utf-8 -*-
from sistercities.venv.src.pywikibot import pywikibot
from pywikibot import pagegenerators as pg
import wikitextparser
from pathlib import Path
import timeit
import json
from contextlib import suppress

de_citylist = []
my_file = Path('list_de_cities.txt')


countries_query = 'SELECT ?item WHERE {?item wdt:P31 wd:Q3624078 . FILTER NOT EXISTS{?item wdt:P31 wd:Q3024240}}'
continent_query = 'SELECT ?item WHERE { ?item wdt:P31 wd:Q5107 .}'

wikidata_site = pywikibot.Site("wikidata", "wikidata")
generator = pg.WikidataSPARQLPageGenerator(countries_query, site=wikidata_site)

generator_countinet = pg.WikidataSPARQLPageGenerator(continent_query, site=wikidata_site)

filteredQIDs = list(generator)
filteredQIDs.extend(list(generator_countinet))

#remove possible duplicates inside a list
#source http://stackoverflow.com/a/7961391
def remove_duplicates(l):
    return list(set(l))

def CityFind(cityname):
    wikipedia_list =[]
    wikidata_list = []


    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    wikipedia_object = pywikibot.Page(de_wikipedia, cityname)
    if wikipedia_object.isRedirectPage():
        wikipedia_object = wikipedia_object.getRedirectTarget()

    wikidata_object = pywikibot.ItemPage.fromPage(wikipedia_object)

    #fetch wikidata list from wikidata object
    if 'P190' in wikidata_object.claims:
        for city in wikidata_object.claims['P190']:
            wikidata_list.append(city.target)


    #fetch links out of wikipedia article
    section_keywords = [ 'Städtepartnerschaften', 'Städtepartnerschaft',
                         'Schwesterstädte', 'Partnerstädte',
                         'Partnerschaften', 'Gemeindepartnerschaft', 'Partnerstadt']

    #parse wikitext to wikitextparser to read through text
    wt = wikitextparser.parse(wikipedia_object.text)
    for section in wt.sections:
        #limit sectionnames to avoid blank space missmatches
        sectionnamestrip = section.title.strip()

        # search over keywords
        for keyword in section_keywords:
            if sectionnamestrip.find(keyword) != -1:
                print("get wikilinks inside the section::")
                #possible city  -> get wikidata object
                if section.wikilinks:
                    #extract wikilinks inside the section sister city
                    for wikilink in section.wikilinks:
                        #filter out section keywords
                        if wikilink.target in section_keywords:
                            pass
                        else:
                            with suppress(Exception):
                                wikilinkarticle = pywikibot.Page(de_wikipedia, wikilink.target)
                                if wikilinkarticle.pageid !=0:
                                    if wikilinkarticle.isRedirectPage():
                                        wikilinkarticle = wikilinkarticle.getRedirectTarget()
                                    wikilinkarticle = pywikibot.ItemPage.fromPage(wikilinkarticle)
                                    if wikilinkarticle in filteredQIDs:
                                        pass
                                    else:
                                        wikipedia_list.append(wikilinkarticle)
                                        wikipedia_list= remove_duplicates(wikipedia_list)

                                else:
                                    if 'Datei' in wikilink.target:
                                        pass
                                    else:
                                        print('missing page for '+wikilink.target)

                if section.templates:
                    for template in section.templates:
                        template_blacklist = ['Internetquelle', 'Positionskarte+', 'Positionskarte~', 'Nachbargemeinden','Literatur']
                        if template.name.strip() in template_blacklist:
                            pass
                        else:
                            for argument in template.arguments:
                                if argument.value != '#':
                                    wikilinkarticle = pywikibot.Page(de_wikipedia, argument.value)
                                    if wikilinkarticle.pageid != 0:
                                        if wikilinkarticle.isRedirectPage():
                                            wikilinkarticle = wikilinkarticle.getRedirectTarget()
                                        wikidataarticle = pywikibot.ItemPage.fromPage(wikilinkarticle)
                                        if wikidataarticle in filteredQIDs:
                                            pass
                                        else:
                                            wikipedia_list.append(wikidataarticle)
                                            wikipedia_list = remove_duplicates(wikipedia_list)
                                        #TODO refactore to get article methode
                break
    print('wikipedi: ', end='')
    print(wikipedia_list)
    print('wikidata: ',end='')
    print(wikidata_list)

    merge = set(wikipedia_list).intersection(wikidata_list)
    print("intersection:", end='')
    print(merge)
    print('missing on wikipedia: ', end='')
    wikipedia_missing = set(wikidata_list) - set(wikipedia_list)
    print(wikipedia_missing)
    print('missing on wikidata: ', end='')
    wikidata_missing = set(wikipedia_list) - set(wikidata_list)
    print(wikidata_missing)
    #return (wikipedia_list, wikidata_list)



def downloadFile():
    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    de_citylist = 'Liste_der_Städte_in_Deutschland'
    text_file = open("list_de_cities.txt", "w")
    text_file.write(pywikibot.Page(de_wikipedia, de_citylist).text)
    text_file.close()

if my_file.is_file():

    #print('file exist')
    with open('list_de_cities.txt', 'r') as myfile:

        wt = wikitextparser.parse(myfile.read())
        table0 = wt.tables[1]
        data0 = table0.getdata()

        filterarray = [
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
            'Kategorie:Liste (Städte nach Staat)',
            'Liste der 100 flächengrößten Städte und Gemeinden Deutschlands'
        ]

        for cityname in wt.wikilinks:
            if cityname.target not in filterarray:
                de_citylist.append(cityname.target)

else:
    downloadFile()

print(str(len(de_citylist))+' cities in list')
print(de_citylist[1900:1920])
start = timeit.default_timer()
for city in de_citylist[1900:1920]:
    print(city)
    CityFind(city)

stop = timeit.default_timer()

print('runtime: '+str(stop - start))