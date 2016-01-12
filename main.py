import sys, urllib.robotparser, urllib.request, re

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
    for x in a:
        print(x)

    for ref in re.findall('(src|href)="(\S+)"', site_str):
        ref = ref[1]
        if ref.startswith('htt'):
            wynik[ref] = True
            continue
        if '.' in ref:
            continue
        if ref.startswith('/'):
            ref = "{0}{1}".format(link , ref)
            wynik[ref]=True

    for l in wynik.keys():
        print (l)


else:
    print("Nie moze!")

print(">>>>" + link + "<<<<")
