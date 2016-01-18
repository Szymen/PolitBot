import sys, urllib.robotparser, urllib.request, re

#TODO remember about variables that are set as global.



def check_server_introduction(server_response):
    #print ('.getheaders()', server_response.getheaders())
    if server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' and server_response.getheader('Server') != 'None' : #TODO check the rest of headers
        print ('Ładnie się przedstawia = )')



def check_robots(host):   #this part has to be reworked

    global can_browse
    global robots_broken
    can_browse = True
    robots_broken = True
    global rp
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url( host + 'robots.txt')  #tu wrzuca się hosta w link

    try:
        rp.read()

        can_browse = rp.can_fetch("*", host)

        return rp
    except Exception:       #catches exception as it can`t open and read non existing robots.txt, so everything is allowed
        #print( "rp.read() nie dziala : (" )
        can_browse = True #it will be easier and more secure to use it in next "if" so i just set it true. no robots means doors open : )
        robots_broken = True
def look_for_links(page_in_string):

    global out_host
    global in_host
    out_host = {}
    in_host = {}

    no_follow = False
    #TODO make good meta-tag behavior

    if re.findall('meta.*robots.*noindex' ,page_in_string):
        print ("Nie indeksujemy strony!")
        no_index = True
        return False  #should end
    if re.findall('meta.*robots.*nofollow' ,page_in_string):
        print ("Nie idziemy stąd dalej!!")
        no_follow = True
        return True
    if re.findall('meta.*robots.*none' ,page_in_string):
        print ("Nie indeksujemy i nie idziemy dalej!!")
        no_follow = True
        return False
    if not no_follow:

        for ref in re.findall('(src|href)="(\S+)"', page_in_string):
            ref = ref[1]

            if ( not ref.endswith('.html') ) and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                    continue #ignore it. it`s crap.

            if ref.startswith('/'): #it`s link to some sub-site
               ref = "{0}{1}".format(link , ref)
               if robots_broken:
                    #print("Can fetch! << robots_broken")
                    in_host[ref] = True
               elif rp.can_fetch('*', ref):
                    #print("Can fetch!")
                    in_host[ref] = True

            elif ref.startswith('htt'): #either http or https; link to other site
                if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                    continue #ignore it. it`s crap.

                if ref.startswith(link):
                    in_host[ref] = True
                    continue #don`t want to be added into out links
                out_host[ref]=True #maybe other data structure?
                continue #everything is done

            elif ref.endswith('.html'): #another type of links  #dont`t know if this part is working
                in_host[ base_url + '/'+ ref] = True
        return True
def set_correct_url(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        return 'http://' + url
    else:
        return url
def get_site_content():
    if  can_browse or robots_broken:
    #print("Moze!")
        req = urllib.request.Request(
                base_url,
                data = None,
                headers = {
                 'User-Agent': 'PolitBot ( http://edi.iem.pw.edu.pl/~maslowss/PolitBot/index.html )',  # gdzies tu sie psuje ; (; przecinki? albo cos z adresem strony, to ostatnio zmieniałem
                }
        )
        resp  = urllib.request.urlopen(req)

        check_server_introduction(resp)
        return str( resp.read() )
    else:
        #print ('Nie moze!')
        return '' #empty string; it`s not bug :D
def print_links():
    a = 0
    print('Inside : ')
    for l in in_host.keys():
        print (l)
        a+=1
    print('Ogolem linkow wewnatrz : ',a)
    a = 0
    print('Outside : ')
    for l in out_host.keys():
        print (l)
        a+=1
    print('Ogolem linkow zewnatrz : ',a)
def crawl(start_link):
    global base_url
    base_url = set_correct_url(link)
    rp = check_robots(link)
    site_str = get_site_content()
    if look_for_links(site_str): #True if can browse in them. If false then, cant
        #print_links()
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

crawl(link)
print ('Link z którego wchodzimy :',base_url)




