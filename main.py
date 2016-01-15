import sys, urllib.robotparser, urllib.request, re


### to being considered:
### what to do with found links and where and how should they be stored. If everything together, or those to another host in some "higher" dict/set


link = sys.argv[1]
#link = 'https://www.facebook.com/'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/test.html'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/PolitBot/forbid.html'


if not (link.startswith("http://") or link.startswith("https://")):
    link = "http://" + link
print (link)

rp = urllib.robotparser.RobotFileParser()
rp.set_url(link + 'robots.txt')  #tu wrzuca się hosta w link

try:
    rp.read()
    can_browse = rp.can_fetch("*", link)
except Exception:       #catches exception as it can`t open and read non existing robots.txt, so everything is allowed
    #print( "rp.read() nie dziala : (" )
    can_browse = True
if can_browse:
    print("Moze!")
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



    wynik = {}
    #links = re.findall('"(https?://.*?)"', site_str )
    print ("Linki ktore znaleziono : " )
    #print( links )
    #print("Linki posrednie: ")
    #print (re.findall('(src|href)="(\S+)"', site_str))
    a = re.findall('(src|href)="(\S+)"', site_str)

    #for x in a:
    #    print(x)

    for ref in re.findall('(src|href)="(\S+)"', site_str):
        ref = ref[1]
        if ref.startswith('/'): #it`s link to some sub-site
            ref = "{0}{1}".format(link , ref)
            if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                continue #ignore it. it`s crap.
            #print (ref)
            #if rp.can_fetch('*', ref):
            wynik[ref] = True

        elif ref.startswith('htt'): #either http or https
            if not ref.endswith('.html') and ref.split('/').__len__() > 3 and '.' in  ref.split('/')[ref.split('/').__len__()-1] : #it`s probably css or jpg or whateva; ends up with .../<random>.<sth>
                continue #ignore it. it`s crap.

            wynik[ref]=True #maybe other data structure?
            continue #everything is done

        if '.' in ref:  # we want to delete all shitty css and jpg`s
            continue

    for l in wynik.keys():
        print (l)


else:
    print("Nie moze!")

print(">>>>" + link + "<<<<")
