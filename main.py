import sys, urllib.robotparser, urllib.request, re


### to being considered:
### what to do with found links and where and how should they be stored. If everything together, or those to another host in some "higher" dict/set


link = sys.argv[1]
#link = 'https://www.facebook.com/'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/test.html'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/PolitBot/forbid.html'


if not (link.startswith("http://") or link.startswith("https://")):
    link = "http://" + link
print ('Link z którego wchodzimy :',link)

rp = urllib.robotparser.RobotFileParser()
rp.set_url(link + 'robots.txt')  #tu wrzuca się hosta w link

try:
    rp.read()
    can_browse = rp.can_fetch("*", link)
except Exception:       #catches exception as it can`t open and read non existing robots.txt, so everything is allowed
    #print( "rp.read() nie dziala : (" )
    can_browse = True
    robots_broken = True
if  can_browse or robots_broken:
    #print("Moze!")
    req = urllib.request.Request(
            link,
            data = None,
            headers = {
                'User-Agent': 'PolitBot ( http://edi.iem.pw.edu.pl/~maslowss/PolitBot/index.html )',
            }
    )
    resp  = urllib.request.urlopen(req)
    site_str = str( resp.read() )

    if re.findall('meta.*robots.*noindex' ,site_str):
        print ("Nie indeksujemy strony!")

    if re.findall('meta.*robots.*nofollow' ,site_str):
        print ("Nie idziemy stąd dalej!!")

    if re.findall('meta.*robots.*none' ,site_str):
        print ("Nie indeksujemy i nie idziemy dalej!!")

    out_host = {}
    in_host = {}  # <====== important!! result being initialised here!!!!!!

    #links = re.findall('"(https?://.*?)"', site_str )  #probably will be erased, but don`t have time to look at it, lel
    #print ("Linki ktore znaleziono : " )
    #print( links )
    #print("Linki posrednie: ")
    #print (re.findall('(src|href)="(\S+)"', site_str))
    #a = re.findall('(src|href)="(\S+)"', site_str)

    #for x in a:
    #    print(x)

    for ref in re.findall('(src|href)="(\S+)"', site_str):
        ref = ref[1]
        if ref.startswith('/'): #it`s link to some sub-site
            ref = "{0}{1}".format(link , ref)
            if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                continue #ignore it. it`s crap.
            #print ('>>>>>',ref)
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
else:
    print("Nie moze!")

#print(">>>>" + link + "<<<<")
