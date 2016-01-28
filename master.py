import scraper, queue, threading, time

class Master():

    def __init__(self):
        self.checked = set()
        self.not_seen = queue.Queue()
        self.scrap_res_queue = queue.Queue()
        self.scrapers = []
        self.SCRAPER_LIMIT = 5
        self.free_scrapers = queue.Queue()
        self.queueLock = threading.Lock()

    def update_schedule(self):
        if self.scrap_res_queue.empty():
            return
        self.queueLock.acquire()
        data = self.scrap_res_queue._get()
        self.queueLock.release()
        #print ('<Master>: dostalem : ', data)
        for x in data:
            if not self.checked.__contains__(x):
                self.not_seen.put(x)
                self.checked.add(x)

    def crawl(self,seed):
        print ('Wywolano z seed =',seed)
        self.checked.add(seed)
        self.not_seen._put(seed)
        while True:
            #print(threading.active_count(),"<<<<< ilosc watkow")
            if threading.active_count() < self.SCRAPER_LIMIT + 1 and (not self.not_seen.empty()): #this thread count too
                self.queueLock.acquire()
                new_scraper = scraper.Scraper(self.not_seen._get(),self.scrap_res_queue,threading.active_count())
                self.queueLock.release()
                new_scraper.start()
                self.scrapers.append(new_scraper)
            time.sleep(1)
            self.update_schedule()


