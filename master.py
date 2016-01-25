import scraper, queue, threading, time

class Master():

    koniec = False

    def __init__(self):
        self.checked = set()
        self.not_seen = set()

    def magia(self):
        queue_ins = []
        scrap_res_queue = queue.Queue()
        #for i in range(0,100,2):
        #    queue_ins.append(i)
        #    scrap_res_queue.put(i)
        #print('Zawartosc kolejki :',queue_ins)
        scrapers = []
        scrapers.append(scraper.Scraper('ilo.pl',scrap_res_queue,1))

        for x in scrapers:
            x.start()

        print('Wystartowal!')

        print('Koniec zabawy')

        while not scrap_res_queue.empty():
            print('W kolejce ',scrap_res_queue._get())
#print('Zaczynamy')


Master().magia()

#print('>>>>Koniec<<<<')