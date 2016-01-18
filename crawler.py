import sys, urllib.robotparser, urllib.request, re

#TODO needs to be rewieved as was built for down to up.


class Crawler:

    def __init__(self):
        self.robots_broken = True
        self.can_browse = True
        self.rp = None
        self.out_host = set()
        self.in_host = set()
        self.no_follow = False
        self.base_url = ''

    def check_server_introduction(self,server_response):
        #print ('.getheaders()', server_response.getheaders())
        if server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' : #TODO check the rest of headers
            print ('Ładnie się przedstawia = )')

    def check_robots(self, host):   #this part has to be reworked
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url( host + 'robots.txt')  #tu wrzuca się hosta w link
        try:
            rp.read()
            self.can_browse = rp.can_fetch("*", host)
            return rp
        except Exception:       #catches exception as it can`t open and read non existing robots.txt, so everything is allowed
            #print( "rp.read() nie dziala : (" )
            self.can_browse = True #it will be easier and more secure to use it in next "if" so i just set it true. no robots means doors open : )
            self.robots_broken = True
    def look_for_links(self, page_in_string):

        #TODO make good meta-tag behavior

        if re.findall('meta.*robots.*noindex' ,page_in_string):
            print ("Nie indeksujemy strony!")
            self.no_index = True
            return False  #should end
        if re.findall('meta.*robots.*nofollow' ,page_in_string):
            print ("Nie idziemy stąd dalej!!")
            self.no_follow = True
            return True
        if re.findall('meta.*robots.*none' ,page_in_string):
            print ("Nie indeksujemy i nie idziemy dalej!!")
            self.no_follow = True
            return False
        if not self.no_follow:

            for ref in re.findall('(src|href)="(\S+)"', page_in_string):
                ref = ref[1]

                if ( not ref.endswith('.html') ) and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                        continue #ignore it. it`s crap.

                if ref.startswith('/'): #it`s link to some sub-site
                   ref = "{0}{1}".format(link , ref)
                   if self.robots_broken:
                    #print("Can fetch! << robots_broken")
                        self.in_host.add(ref)
                   elif self.rp.can_fetch('*', ref):
                        #print("Can fetch!")
                        self.in_host.add(ref)

                elif ref.startswith('htt'): #either http or https; link to other site
                    if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                        continue #ignore it. it`s crap.

                    if ref.startswith(link):
                        self.in_host.add(ref)
                        continue #don`t want to be added into out links
                    self.out_host.add(ref) #maybe other data structure?
                    continue #everything is done

                elif ref.endswith('.html'): #another type of links  #dont`t know if this part is working
                    self.in_host.add( self.base_url + '/'+ ref)
            return True

    def set_correct_url(self, url):
        if not (url.startswith("http://") or url.startswith("https://")):
            return 'http://' + url
        else:
            return url

    def get_site_content(self ):
        if  self.can_browse or self.robots_broken:
            #print("Moze!")
            req = urllib.request.Request(
                    self.base_url,
                    data = None,
                    headers = {
                     'User-Agent': 'PolitBot ( http://edi.iem.pw.edu.pl/~maslowss/PolitBot/index.html )',  # gdzies tu sie psuje ; (; przecinki? albo cos z adresem strony, to ostatnio zmieniałem
                    }
            )
            resp  = urllib.request.urlopen(req)
            self.check_server_introduction(resp)
            return str( resp.read() )
        else:
            #print ('Nie moze!')
            return '' #empty string; it`s not bug :D
    def print_links(self):
        a = 0
        print('Inside : ')
        for l in self.in_host:
            print (l)
            a+=1
        print('Ogolem linkow wewnatrz : ',a)
        a = 0
        print('Outside : ')
        for l in self.out_host:
            print (l)
            a+=1
        print('Ogolem linkow zewnatrz : ',a)
    def crawl(self, start_link):

        self.base_url = self.set_correct_url(link)
        self.rp = self.check_robots(link)
        site_str = self.get_site_content()
        if self.look_for_links(site_str): #True if can browse in them. If false then, cant
            self.print_links()
            pass

    ## TODO look for forms at the page/application?
    ## TODO check if easy/default passwords can give me acces : 3
    ## TODO easy SQL injection, ahh think of it as late todo :D


### to being considered:
### what to do with found links and where and how should they be stored. If everything together, or those to another host in some "higher" dict/set

## GENERAL TODO add request/time limitation
## givem limit is x/hour ;why not make it other?



link = sys.argv[1]
#link = 'https://www.facebook.com/'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/test.html'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/PolitBot/forbid.html'
#link = 'isod.ee.pw.edu.pl'

a = Crawler()
a.crawl(link)
print ('Link z którego wchodzimy :', a.base_url)




