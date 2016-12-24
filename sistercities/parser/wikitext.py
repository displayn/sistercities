# -*- coding: utf-8 -*-

from sistercities.venv.src.pywikibot import pywikibot
import wikitextparser as wtp
from pathlib import Path
import timeit

#https://de.wikipedia.org/wiki/Liste_der_Städtelisten_nach_Ländern

de_citylist = []
my_file = Path('list_de_cities.txt')

def downloadFile():
    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    de_citylist = 'Liste_der_Städte_in_Deutschland'
    text_file = open("list_de_cities.txt", "w")
    text_file.write(pywikibot.Page(de_wikipedia, de_citylist).text)
    text_file.close()

def checkObjectExist(cityname):
    wikdata_cities = []
    wikipedia_cities = []

    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    page = pywikibot.Page(de_wikipedia, cityname)

    text = page.text

    #find section
    wt = wtp.parse(text)

    section_keywords = [
        'Städtepartnerschaften',
        'Städtepartnerschaft',
        'Schwesterstädte',
        'Partnerstädte',
        'Partnerschaften',
        'Gemeindepartnerschaft'
    ]

    for section in wt.sections:
        sectionnamestrip = section.title.strip()

        # search over keywords
        for keyword in section_keywords:
            if sectionnamestrip.find(keyword) != -1:

                print('FOUND Section!:' + sectionnamestrip)
                if section.external_links:
                    print(section.external_links)
                # grep wikilinks from the section of sister cities
                print("get wikilinks inside the section::")
                for wikilink in section.wikilinks:
                    if wikilink != cityname:
                        link = pywikibot.Page(de_wikipedia, wikilink.target)
                        if link.pageid !=0:
                            if link.previous_revision_id < 0:
                                urls = wtp.parse(link.text)
                                for url in urls.wikilinks:
                                    link = pywikibot.Page(de_wikipedia, url.target)

                            item = pywikibot.ItemPage.fromPage(link)
                            item.get()

                            if 'en' in item.descriptions:
                                en_description = item.descriptions['en']

                                list_labels = ['village','town', 'capital', 'city-state', 'city', 'municipality', 'comune', 'commune', 'human settlement in Denmark']
                                list_de_labels =['Stadt']
                                for label in list_labels:
                                    if en_description.find(label) != -1:
                                        print(wikilink.target+' is a '+label)

                            elif 'de' in item.descriptions:
                                de_description = item.descriptions['de']
                                list_de_labels = ['Stadt']
                                for label in list_de_labels:
                                    if de_description.find(label) != -1:
                                        print(wikilink.target+' is a '+label+' Missing English LABEL!')

                            else:
                                print('missing label for de or en @'+wikilink.target)
                                if 'P31' in item.claims:  # request instance of claims
                                    instances = (item.claims['P31'])
                                    if 'Q515' or 'Q747074' in instances:
                                        print(wikilink.target+' is a instance of city')
                                #add check for sister citie property check
                                if 'P190' in item.claims:
                                    sistercities_list = (item.claims['P190'])
                                    if item.getID in sistercities_list:
                                        print('found a connection between'+wikilink.target+'and' +cityname)

                        else:
                            print(wikilink.target+" don't exist in the de wikipedia")
                break

    if page.data_repository.has_data_repository:
        print(cityname + ' has a a object |', end="")

        try:
            # connect to wikidata object
            item = pywikibot.ItemPage.fromPage(page)
            print('connected to wikidata object: ' + item.getID(), end="")
            item.get() #request data

            if item.claims:  # request claims
                if 'P190' in item.claims:  # request sister city property
                    sistercities = (item.claims['P190'])
                    print(' | '+str(len(sistercities)) + ' sister cities: ', end="")
                    for sistercity in sistercities:
                        print(sistercity.getTarget(), end="")
                    #print("sister cities", len(sistercities), end="")
                    #print(item.claims['P190'][0].getTarget())
                    #pprint.pprint(sistercities)
        except OSError:
            pass
        print('')
    else:
        print(cityname + ' has no object')


if my_file.is_file():

    #print('file exist')
    with open('list_de_cities.txt', 'r') as myfile:

        wt = wtp.parse(myfile.read())
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
            'Kategorie:Liste (Städte nach Staat)'
        ]

        for cityname in wt.wikilinks:
            if cityname.target not in filterarray:
                de_citylist.append(cityname.target)

else:
    downloadFile()

print(str(len(de_citylist))+' cities in list')
print(de_citylist[514:515])
start = timeit.default_timer()
for city in de_citylist[514:515]:
    checkObjectExist(city)

stop = timeit.default_timer()

print('runtime: '+str(stop - start))