#!/usr/bin/python3
""" Algoritmes gebruikt voor het vinden van n = p * q (Setoc Wiskunde) """

# importeer extra modules
import queue
import threading
import time

_STOP_THREADS = False # Stop vlag voor threads

def isqrt(n):
    """ Wortel trekken via het algoritme van Newton """
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def is_prime(number):
    """ Kijkt of het getal priem is """
    for i in range(3, number):
        if number % i == 0:
            return False
    return True

def is_prime_fast(number):
    """ Kijkt snel of het getal deelbaar is door de eerste paar priemgetallen """
    for i in [2, 3, 5, 7, 13]:
        if number % i == 0:
            return False
    return True

def get_pq_max_min(nbits):
    """ Minimum en maximum p en q met nbits vb. 2048 """
    halfbits = nbits // 2
    shift = halfbits // 16
    
    pbits = halfbits + shift
    qbits = halfbits - shift

    return (pow(2,pbits), pow(2,qbits), pow(2,pbits-1), pow(2,qbits-1)) # (pmax,qmax,pmin,qmin)

def get_pq_max_min_from_n(n, pmax, qmax, pmin, qmin):
    """ Minimum en maximum p en q met n """
    return (n//qmin, n//pmin , n//qmax , n//pmax) # (pmax,qmax,pmin,qmin)

def get_final_pq_max_min(n, pmax1, qmax1, pmin1, qmin1, pmax2, qmax2, pmin2, qmin2):
    """
    getpqmaxmin() en getpqmaxminfromn() conbineren.
    Eerst getpqmaxmin() [1] en dan getpqmaxminfromn() [2]
    """
    # initialisatie van variabelen
    worteln = isqrt(n)
    pmax = 0
    qmax = 0
    pmin = 0
    qmin = 0

    # pmax
    if pmax1 < pmax2:
        pmax = pmax1
    else:
        pmax = pmax2

    # pmin
    if pmin1 > pmin2:
        pmin = pmin1
    else:
        pmin = pmin2
    
    # qmax
    if qmax1 < qmax2:
        qmax = qmax1
    else:
        qmax = qmax2

    # qmin
    if qmin1 > qmin2:
        qmin = qmin1
    else:
        qmin = qmin2

    # Check de wortel na
    if pmax < worteln:
        pmax = worteln
    if qmax > worteln:
        qmax = worteln
    if pmin < worteln:
        pmin = worteln
    if qmin > worteln:
        qmin = worteln
    
    return (pmax,qmax,pmin,qmin)

def get_meest_interessant(pmax,qmax,pmin,qmin):
    """ Returneerd welk priemgetal het snelst kans geeft op winst (p,q) """
    if (pmax - pmin) < (qmax - qmin):
        return (True, False) # (p,q)
    else:
        return (False, True) # (p,q)

def zoek_pq_lus(n, max, min, aantal_threads = 1):
    """ Brute force van verkleind gebied """

    global _STOP_THREADS # Stop vlag voor threads

    index = (min | 1) - 2 # Zorg dat index oneven start en klaar is voor de lus
    worteln = isqrt(n)
    mQueue = queue.SimpleQueue()

    print("[*] Begin van lus met n= {}, max= {}, min= {}, index= {}".format(n,max,min,index))

    def loop(worteln, max, min, threadid, mQueue):
        """ Functie op een thread """
        global _STOP_THREADS

        index = (min | 1) - 2 # Zorg dat index oneven start en klaar is voor de lus

        while index < max and not _STOP_THREADS: # Checken of er niet gestopt moet worden
            index += 2 # index updaten

            print("[{}] {}de iteratie".format(threadid,index-min))

            if not is_prime_fast(index): # Gemakkelijk te delen getallen verwerpen
                continue
            
            if n % index != 0: # Niet deelbaar door n verwerpen
                continue
            
            if is_prime(index): # Mogelijke candidaad voor oplossing
                print("Mogelijk gevonden resultaat {}".format(index))
                mQueue.put(index) # uiteindelijk resultaat versturen naar main_thread

    class mThread(threading.Thread):
        """ Helper classe voor de multithreading """
        def __init__(self, worteln, max, min, threadid, mQueue):
            super(mThread, self).__init__()
            self.worteln = worteln
            self.max = max
            self.min = min
            self.threadid = threadid
            self.mQueue = mQueue

        def run(self):
            print("Starten van thread ({}) met tmax= {}, tmin= {}".format(self.threadid, self.max, self.min))
            loop(self.worteln,self.max,self.min,self.threadid,self.mQueue)
            print("Stoppen van thread: {}".format(self.threadid))
            
    twork = (max-min) // aantal_threads # aantal nummers dat elke thread moet verwerken
    threads = [] # Lijst van alle threads

    for i in range(0, aantal_threads):
        tmax = min + ((i+1) * twork) # max limiet voor elke thread
        tmin = min + ((i) * twork)   # min limiet voor elke thread
        thread = mThread(worteln,tmax,tmin,"t"+str(i), mQueue)
        threads.append(thread)
    
    time_start = time.time() # Bereken de starttijd

    _STOP_THREADS = False # Zorg dat de threads mogen draaien

    for thread in threads:
        thread.start() # Start met rekenen op andere threads
    try:
        while mQueue.empty(): # wacht tot er een getal is gevonden
            pass
    except KeyboardInterrupt:
        print("Voortijdig gestopt na {}s".format(time.time() - time_start))
        # Stop al de threads
        _STOP_THREADS = True # Geef signaal door

    # Priemgetal gevonden in mQueue
    time_stop = time.time() # Stop de timer
    print("[*] {} (mogelijk oplossingen gevonden in {}s)".format(mQueue.qsize(), time_stop - time_start))
    pq = mQueue.get(block=False) # Haal het gevonden priemgetal op

    # print("Priemgetal gevonden in {}s,\npq = {}".format(time_stop - time_start, pq))

    # Stop al de threads
    _STOP_THREADS = True # Geef signaal door

    return pq

def get_max_iter(max, min):
    """ Geeft het aantal nummers weer die moeten overlopen worden om een priemgetal te bereiken """
    return (max - min) // 2

def compare(p,q,pmax,qmax,pmin,qmin):
    """ Kijkt of p en q binnen de grenzen vallen ==> Testen van algoritme """
    print("p < pmax => {}".format(p < pmax))
    print("q < qmax => {}".format(q < qmax))
    print("p > pmin => {}".format(p > pmin))
    print("q > qmin => {}".format(q > qmin))

def init(n, nbits, aantal_threads = 1):
    """ Voert bovenstaande functies uit en zoekt naar een priemgetal """
    pq1 = get_pq_max_min(nbits)
    pq_from_n = get_pq_max_min_from_n(n, *pq1)

    final = get_final_pq_max_min(n, *pq1, *pq_from_n)

    result_pq = 0 # uiteindelijke uitkomst
    if get_meest_interessant(*final) == (True, False):
        # p is het interessantst
        print("[*] p is het interessantst met {} mogelijkheden".format(final[0] - final[2]))
        result_pq = zoek_pq_lus(n, final[0], final[2], aantal_threads)
    else:
        # q is het interessantst
        print("[*] q is het interessantst met {} mogelijkheden".format(final[1] - final[3]))
        result_pq = zoek_pq_lus(n, final[1], final[3], aantal_threads)
    
    print("[*] Gevonden resultaat is {}".format(result_pq))

    return result_pq

if __name__ == "__main__":
    """ Een test van het algoritme met 16 bits """
    init(43931, 16, 3) # p = 223; q = 197
