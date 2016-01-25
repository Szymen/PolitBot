import scraper, queue, threading, time

class Master():

    def __init__(self):
        self.checked = set()
        self.not_seen = queue.Queue()
        self.scrap_res_queue = queue.Queue()
        self.scrapers = []
        self.SCRAPER_AMOUNT = 10
        self.free_scrapers = queue.Queue()

    def crawl(self, seed):
        self.checked.add(seed)
        self.not_seen._put(seed)
        for i in range (0, self.SCRAPER_AMOUNT):
            self.scrapers.append(scraper.Scraper(self.not_seen.get(), '', i , self.free_scrapers))
            self.free_scrapers._put(i)

        while True:

            if not self.free_scrapers.empty() and not self.not_seen.empty() : #means, we can afford more workers and have something to process
                self.scrapers[self.free_scrapers._get()] = scraper.Scraper( self.not_seen.get(), self.scrap_res_queue, self.scrapers.__len__() ))
                self.scrapers[self.scrapers.__len__()-1].start()

            if not self.scrap_res_queue.empty():
                self.update_schedule()

    def update_schedule(self):
        queueLock = threading.Lock()
        queueLock.acquire()
        data = self.scrap_res_queue._get()
        queueLock.release()
        for x in data:
            if not self.checked.__contains__(x):
                self.not_seen.put(x)
                self.checked.add(x)



print('Zaczal!')
a = Master()
a.crawl('wololol.gov')
print ('Skonczyl!')