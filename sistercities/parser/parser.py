# -*- coding: utf-8 -*-
from sistercities.venv.src.pywikibot import pywikibot
from pywikibot import pagegenerators as pg
import wikitextparser
from pathlib import Path
import timeit
from contextlib import suppress
import networkx as nx
from networkx.readwrite import json_graph
import json

de_citylist = []
sourcelist = Path('list_de_cities.txt')

query_combine = '''SELECT ?item WHERE {
                  {
                    ?item wdt:P31 wd:Q3624078 .
                    FILTER NOT EXISTS{?item wdt:P31 wd:Q3024240}
                  }
                  UNION {
                    ?item wdt:P31 wd:Q1221156 .
                    FILTER NOT EXISTS{?item wdt:P31 wd:Q3024240} .
                    FILTER NOT EXISTS{?item wdt:P31 wd:Q133442}.
                    }
                  UNION {
                     ?item wdt:P31 wd:Q896375 .
                    }
                  UNION {
                  ?item wdt:P31 wd:Q245065 .
                  }
                  UNION {
                     ?item wdt:P31 wd:Q5107 .
                    }
                  UNION {
                     ?item wdt:P31 wd:Q1048835 .
                   }
                   UNION {
                     ?item wdt:P31 wd:Q16110 .
                   }
                   UNION {
                     ?item wdt:P31 wd:Q15089 .
                   }
                   UNION {
                    ?item wdt:P31 wd:Q6465 .
                   }
                   UNION {
                    ?item wdt:P31 wd:Q193622 .
                    }
                }'''

wikidata_site = pywikibot.Site("wikidata", "wikidata")
generator = pg.WikidataSPARQLPageGenerator(query_combine, site=wikidata_site)

filteredQIDs = list(generator)


def remove_duplicates(l):
    # remove possible duplicates inside a list
    # source http://stackoverflow.com/a/7961391
    return list(set(l))


def city_find(citylink):
    wikipedia_list = []
    wikidata_list = []

    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    wikipedia_object = pywikibot.Page(de_wikipedia, citylink)
    if wikipedia_object.isRedirectPage():
        wikipedia_object = wikipedia_object.getRedirectTarget()

    wikidata_object = pywikibot.ItemPage.fromPage(wikipedia_object)

    if 'P190' in wikidata_object.claims:
        # fetch wikidata list from wikidata object
        for city in wikidata_object.claims['P190']:
            wikidata_list.append(city.target)

    # fetch links out of wikipedia article
    section_keywords = ['Städtepartnerschaften', 'Städtepartnerschaft',
                        'Schwesterstädte', 'Partnerstädte',
                        'Partnerschaften', 'Gemeindepartnerschaft', 'Partnerstadt']

    # parse wikitext to wikitextparser to read through text
    wt = wikitextparser.parse(wikipedia_object.text)
    for section in wt.sections:
        # limit sectionnames to avoid blank space missmatches
        sectionnamestrip = section.title.strip()

        # search over keywords
        for keyword in section_keywords:
            if sectionnamestrip.find(keyword) != -1:
                print("get wikilinks inside the section::")

                if section.wikilinks:
                    # possible city  -> get wikidata object

                    for wikilink in section.wikilinks:
                        # extract wikilinks inside the section sister city

                        if wikilink.target in section_keywords:
                            # filter out section keywords
                            pass
                        else:
                            with suppress(Exception):
                                wikilinkarticle = pywikibot.Page(de_wikipedia, wikilink.target)
                                if wikilinkarticle.pageid != 0:
                                    if wikilinkarticle.isRedirectPage():
                                        wikilinkarticle = wikilinkarticle.getRedirectTarget()
                                    wikilinkarticle = pywikibot.ItemPage.fromPage(wikilinkarticle)
                                    if wikilinkarticle in filteredQIDs:
                                        pass
                                    else:
                                        wikipedia_list.append(wikilinkarticle)
                                        wikipedia_list = remove_duplicates(wikipedia_list)
                                else:
                                    if 'Datei' in wikilink.target:
                                        pass
                                    else:
                                        print('missing page for ' + wikilink.target)

                if section.templates:
                    for template in section.templates:
                        template_blacklist = ['sortkey', 'lang', 'Internetquelle', 'Positionskarte+', 'Positionskarte~',
                                              'Nachbargemeinden', 'Literatur', 'Panorama']
                        if template.name.strip() in template_blacklist:
                            pass
                        else:
                            with suppress(Exception):
                                for argument in template.arguments:
                                    if argument.value.strip() != '#':
                                        wikilinkarticle = pywikibot.Page(de_wikipedia, argument.value)
                                        if wikilinkarticle.exists():
                                            if wikilinkarticle.isRedirectPage():
                                                wikilinkarticle = wikilinkarticle.getRedirectTarget()

                                            wikidataarticle = pywikibot.ItemPage.fromPage(wikilinkarticle)
                                            if wikidataarticle in filteredQIDs:
                                                pass
                                            else:
                                                wikipedia_list.append(wikidataarticle)
                                                wikipedia_list = remove_duplicates(wikipedia_list)
                                        else:
                                            print('missing page' + argument.value)

                break
    print('wikipedi: ', end='')
    print(wikipedia_list)
    print('wikidata: ', end='')
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

    city_dict = {'root_city': wikidata_object,
                 'wiki_cities': wikipedia_list,
                 'data_cities': wikidata_list
                 }
    return (city_dict)


def download_file():
    de_wikipedia = pywikibot.Site('de', 'wikipedia')
    de_citylist = 'Liste_der_Städte_in_Deutschland'
    text_file = open("list_de_cities.txt", "w")
    text_file.write(pywikibot.Page(de_wikipedia, de_citylist).text)
    text_file.close()


def write_graph(data, filename):
    fd = open(filename, 'w')
    fd.write(str(data))
    fd.close()


def input_list(filename):
    citylist = []
    with open(filename, 'r') as myfile:
        wt = wikitextparser.parse(myfile.read())

        filterarray = [
            'Stadt', 'Deutschland', 'Gemeinde (Deutschland)',
            'Stadtrecht', 'Land (Deutschland)', 'Liste der flächengrößten Städte und Gemeinden Deutschlands',
            'Liste der Großstädte in Deutschland', 'Liste der Groß- und Mittelstädte in Deutschland',
            'Agglomeration#Deutschland',
            'Liste der größten deutschen Städte', 'Liste der kleinsten Städte in Deutschland nach Einwohnerzahl',
            'Liste der Städte in Brandenburg',
            'Liste der Städte in Mecklenburg-Vorpommern', 'Liste der Städte in Thüringen',
            'Liste der Städte im Saarland',
            'Liste ehemaliger Städte in Deutschland', 'Kategorie:Liste (Gemeinden in Deutschland)',
            'Kategorie:Liste (Städte nach Staat)',
            'Liste der 100 flächengrößten Städte und Gemeinden Deutschlands'
        ]

        for citylink in wt.wikilinks:
            if citylink.target not in filterarray:
                citylist.append(citylink.target)
    return citylist

def add_graph_nodes(data_graph, root_city, wikicities, root_city_attributes):
        #create root node
        data_graph.add_node(root_city.id, root_city_attributes)

        for city in wikicities:
            city.get()
            url = ''
            if city.sitelinks:
                if 'dewiki' in city.sitelinks:
                    url = city.sitelinks['dewiki']
                elif 'enwiki' in city.sitelinks:
                    url = city.sitelinks['enwiki']
                else:
                    url = next(city.sitelinks.__iter__())

            attr_child = {
                'url': url
            }

            # add connection between root city an sister city
            data_graph.add_edge(root_city.id, city.id)
            # create or update node of the sister city
            data_graph.add_node(city.id, attr_child)
        return data_graph

if __name__ == '__main__':

    if sourcelist.is_file():
        de_citylist = input_list('list_de_cities.txt')
    else:
        download_file()
        de_citylist = input_list('list_de_cities.txt')

    dg = nx.DiGraph()
    wg = nx.DiGraph()

    print(str(len(de_citylist)) + ' cities in list')
    print(de_citylist)#[110:121])

    start = timeit.default_timer()
    for city in de_citylist:#[110:121]:
        print(city)

        sistercities = city_find(city)

        root_city = sistercities['root_city']
        wikipedia = sistercities['wiki_cities']
        wikidata = sistercities['data_cities']
        print(root_city.id)

        attr = {'url': city,
                'latest_revision_id': root_city.latest_revision_id,
                'group': 'roots'
                }

        add_graph_nodes(wg, root_city, wikipedia, attr)
        add_graph_nodes(dg, root_city, wikidata, attr)

    write_graph(json.dumps(json_graph.node_link_data(wg)), 'wikipedia.json')
    write_graph(json.dumps(json_graph.node_link_data(dg)), 'wikidata.json')

    stop = timeit.default_timer()
    print('runtime: ' + str(stop - start))
