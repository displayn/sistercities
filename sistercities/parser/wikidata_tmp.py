from sistercities.venv.src.pywikibot import pywikibot as pwb
import wikitextparser
import pprint

de_wikipedia = pwb.Site('de', 'wikipedia')
wikidata = de_wikipedia.data_repository()

#get city name from list
#https://www.wikidata.org/wiki/Q209208

#Aach
cityname = 'Gelsenkirchen'
page = pwb.Page(de_wikipedia, cityname)
if page.previous_revision_id < 0:
    urls = wikitextparser.parse(page.text)
    for url in urls.wikilinks:
        cityname = url.target
        page = pwb.Page(de_wikipedia, cityname)

if page.data_repository.has_data_repository:
    print(cityname+' has a a object |', end="")

    try:
        # connect to wikidata object
        item = pwb.ItemPage.fromPage(page)
        pprint.pprint('connected to wikidata object: '+item.getID())
        #item.get() #request data

        if item.claims: #request claims
            if 'P190' in item.claims: #request sister city property
                sistercities = (item.claims['P190'])
                print("sister length", len(sistercities))
                for city in sistercities:
                    print(city.getTarget())
                #print(item.claims['P190'][0].getTarget())
        pprint.pprint(item)
    except OSError:
        pass
else:
    print(cityname+' has no object')
