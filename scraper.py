import sys, urllib.robotparser, urllib.request, re, threading, time, queue

#TODO needs to be rewieved as was built for down to up.


class Scraper(threading.Thread):

    def __init__(self, start_link , result_queue , ID):
        threading.Thread.__init__(self)
        self.ID = ID
        self.start_link = start_link
        self.robots_broken = True
        self.can_browse = True
        self.rp = None
        self.out_host = set()
        self.in_host = set()
        self.visited = set()
        self.no_follow = False
        self.base_url = ''
        self.result_queue = result_queue
        self.WAIT_TIME = 120 # in secs

    def run( self ):
        print ('Stworzono scrapera! ID:',self.ID, 'zacznie z : ',self.start_link)
        self.set_correct_url(self.start_link)
        self.check_robots(self.base_url)
        self.look_for_links(self.base_url)
        self.send_links()
        return

    def get_links(self):
        return self.in_host
    def check_server_introduction(self,server_response):
        #print ('.getheaders()', server_response.getheaders())
        if server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' : #TODO check the rest of headers
            #print ('Ładnie się przedstawia = )')
            pass
    def check_robots(self, host):   #this part has to be reworked
        tmp = host
        host = ''
        for x in tmp.split('/')[0:3]:
            host += x + '/'
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
    def send_links(self):
        try: ## look at this if send good results
            queueLock = threading.Lock()
            queueLock.acquire()
            self.result_queue.put( tuple(self.out_host) )
            queueLock.release()
        finally:
            queueLock.release
        #print ('<<<<',self.ID,'>>>> wynik:  ', self.out_host )

    def look_for_links(self, site_url):
        #TODO make good meta-tag behavior
        visited = set()
        visited.add(site_url)
        q = queue.Queue()
        q._put(site_url)
        while not q.empty():
            url = q._get()
            print('<<',self.ID,'>> Sciagam kolejna strone : ',url ,'Rozmiar kolejki = ',q._qsize())
            visited.add(url)
            if url.endswith('//'):
                url = url[:-1] #cut second slash off
            try :
                str_page =  self.get_site_content(url)
            except Exception:
                continue # just don`t do anything with this link, lol
            time.sleep(self.WAIT_TIME) # 2 mins, so it won`t spam and so.
            if re.findall('meta.*robots.*noindex' ,str_page):
                #print ("Nie indeksujemy strony!")
                self.no_index = True
                continue  #should end
            if re.findall('meta.*robots.*nofollow' ,str_page):
                #print ("Nie idziemy stąd dalej!!")
                self.no_follow = True
                continue
            if re.findall('meta.*robots.*none' ,str_page):
                #print ("Nie indeksujemy i nie idziemy dalej!!")
                self.no_follow = True
                continue

            for ref in re.findall('(src|href)="(\S+)"', str_page):
                ref = ref[1]

                if ( not ref.endswith('.html') ) and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                        continue #ignore it. it`s crap.

                if ref.startswith('/images') :  #just to make it simplier
                    continue

                if ref.startswith('/'): #it`s link to some sub-site
                   ref = "{0}{1}".format( url , ref)
                   if self.robots_broken:
                    #print("Can fetch! << robots_broken")
                        if not visited.__contains__(ref.split('/')[2]):
                            q._put(ref)
                            visited.add(ref.split('/')[2])
                   elif self.rp.can_fetch('*', ref):
                        #print("Can fetch!")
                        if not visited.__contains__(ref.split('/')[2]):
                            q._put(ref)
                            visited.add(ref.split('/')[2])

                elif ref.startswith('htt'):  #either http or https; link to other site
                    if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                        continue #ignore it. it`s crap.

                    if ref.startswith(self.base_url):
                        if not visited.__contains__(ref.split('/')[2]):
                            q._put(ref)
                            visited.add(ref.split('/')[2])
                            continue #don`t want to be added into out links

                    if not self.base_url.split('/')[2] in ref and not ref.split('/')[2] in self.out_host: # it the essential part of link, without http or www
                        self.out_host.add(ref)
                        continue #everything is done

                elif ref.endswith('.html'): #another type of links  #dont`t know if this part is working
                    if ref.startswith('/'):
                        ref = self.base_url+ref
                    else:
                        ref = self.base_url+'/'+ref
                    if not visited.__contains__(ref.split('/')[2]):
                            q._put(ref)
                            visited.add(ref.split('/')[2])
    def set_correct_url(self, url):
        if not (url.startswith("http://") or url.startswith("https://")):
            self.base_url = 'http://' + url
        else:
                self.base_url = url

    def get_site_content( self, site_url ):
        if  self.can_browse or self.robots_broken:
            #print("Moze!")
            req = urllib.request.Request(
                    site_url,
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

    ## TODO look for forms at the page/application?
    ## TODO check if easy/default passwords can give me acces : 3
    ## TODO easy SQL injection, ahh think of it as late todo :D
