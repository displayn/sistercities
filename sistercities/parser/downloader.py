from sistercities.venv.src.pywikibot import pywikibot
class Downloader():
    #url artice, wikisystem



    #check if list already exist
        #get rev id from list out of name

    #get current Revision id from List
    def getRevId(language, wikisystem, URL):
        wiki = pywikibot.getSite(language, wikisystem)
        revID = pywikibot.Page(wikisystem, URL)
        return str(revID)

    #download file
    def downloadFile(self, language, wikisystem, URL):
        wiki = pywikibot.Site(language, wikisystem)
        RevID = Downloader.getRevId(self.language, self.wikisystem, self.URL)
        try:
            text_file = open(RevID+'_list_'+self.language+'_cities.txt', 'w')
            text_file.write(pywikibot.Page(self.wiki, self.URL).text)
            text_file.close()
        except OSError:
            pass
