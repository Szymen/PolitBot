import sys, urllib.robotparser, urllib.request, re

link = sys.argv[1]
#link = 'https://www.facebook.com/'
#link = 'http://edi.iem.pw.edu.pl/~maslowss/test.html'

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
    links = re.findall('"(https?://.*?)"', site_str )
    print ("Linki ktore znaleziono : " )
    print( links )

else:
    print("Nie moze!")

print(">>>>" + link + "<<<<")
