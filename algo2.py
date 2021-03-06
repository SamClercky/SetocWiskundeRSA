#!/usr/bin/python3
""" Algoritmes gebruikt voor het vinden van n = p * q (Setoc Wiskunde) """

# importeer extra modules
import queue
import threading
import time
import math
from typing import List

_STOP_THREADS: bool = False  # Stop vlag voor threads


def isqrt(n: int) -> int:
    """ Wortel trekken via het algoritme van Newton """
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def is_prime(number: int) -> bool:
    """ Kijkt of het getal priem is """
    for i in range(3, number):
        if number % i == 0:
            return False
    return True


def is_prime_fast(number: int) -> bool:
    """ Kijkt snel of het getal deelbaar is door de eerste paar priemgetallen """
    for i in [2, 3, 5, 7, 13]:
        if number % i == 0:
            return False
    return True


def get_pq_max_min(nbits: int) -> (int, int, int, int):
    """ Minimum en maximum p en q met nbits vb. 2048 """
    halfbits = nbits // 2
    shift = halfbits // 16

    pbits = halfbits + shift
    qbits = halfbits - shift

    return pow(2, pbits), pow(2, qbits), pow(2, pbits - 1), pow(2, qbits - 1)  # (pmax,qmax,pmin,qmin)


def get_pq_max_min_from_n(n: int, pmax: int, qmax: int, pmin: int, qmin: int) -> (int, int, int, int):
    """ Minimum en maximum p en q met n """
    return n // qmin, n // pmin, n // qmax, n // pmax  # (pmax,qmax,pmin,qmin)


def get_final_pq_max_min(n: int, pmax1: int, qmax1: int, pmin1: int, qmin1: int, pmax2: int, qmax2: int, pmin2: int,
                         qmin2: int) -> (int, int, int, int):
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

    return pmax, qmax, pmin, qmin


def get_meest_interessant(pmax: int, qmax: int, pmin: int, qmin: int) -> (bool, bool):
    """ Returneerd welk priemgetal het snelst kans geeft op winst (p,q) """
    if (pmax - pmin) < (qmax - qmin):
        return True, False  # (p,q)
    else:
        return False, True  # (p,q)


def zoek_pq_lus(n: int, max: int, min: int, aantal_threads: int = 1) -> int:
    """ Brute force van verkleind gebied """

    global _STOP_THREADS  # Stop vlag voor threads

    index: int = (min | 1) - 2  # Zorg dat index oneven start en klaar is voor de lus
    worteln: int = isqrt(n)
    mQueue: queue = queue.SimpleQueue()

    print("[*] Begin van lus met n= {}, max= {}, min= {}, index= {}".format(n, max, min, index))

    def loop(max: int, min: int, threadid: str, mqueue: queue) -> None:
        """ Functie op een thread """
        global _STOP_THREADS

        index: int = (min | 1) - 2  # Zorg dat index oneven start en klaar is voor de lus

        while index < max and not _STOP_THREADS:  # Checken of er niet gestopt moet worden
            index += 2  # index updaten

            print("[{}] ".format(threadid), end='')

            if not is_prime_fast(index):  # Gemakkelijk te delen getallen verwerpen
                continue

            if n % index != 0:  # Niet deelbaar door n verwerpen
                continue

            if is_prime(index):  # Mogelijke candidaad voor oplossing
                print("Mogelijk gevonden resultaat {}".format(index))
                mqueue.put(index)  # uiteindelijk resultaat versturen naar main_thread

        print("[{}] Stoppen van thread op index= {}, max= {}, min= {}".format(threadid, index, max, min))

    class MThread(threading.Thread):
        """ Helper classe voor de multithreading """

        def __init__(self, max: int, min: int, threadid: str, mQueue: queue):
            super(MThread, self).__init__()
            self.max: int = max
            self.min: int = min
            self.threadid: str = threadid
            self.mQueue: queue = mQueue

        def run(self):
            print("Starten van thread ({}) met tmax= {}, tmin= {}".format(self.threadid, self.max, self.min))
            loop(self.max, self.min, self.threadid, self.mQueue)
            print("Stoppen van thread: {}".format(self.threadid))

    twork = (max - min) // aantal_threads  # aantal nummers dat elke thread moet verwerken
    threads: List[MThread] = []  # Lijst van alle threads

    for i in range(0, aantal_threads):
        tmax: int = min + ((i + 1) * twork)  # max limiet voor elke thread
        tmin: int = min + (i * twork)  # min limiet voor elke thread
        thread: thread = MThread(tmax, tmin, "t" + str(i), mQueue)
        threads.append(thread)

    time_start = time.time()  # Bereken de starttijd

    _STOP_THREADS = False  # Zorg dat de threads mogen draaien

    for thread in threads:
        thread.start()  # Start met rekenen op andere threads
    try:
        while mQueue.empty():  # wacht tot er een getal is gevonden
            pass
    except KeyboardInterrupt:
        print("Voortijdig gestopt na {}s".format(time.time() - time_start))
        # Stop al de threads
        _STOP_THREADS = True  # Geef signaal door

    # Priemgetal gevonden in mQueue
    time_stop = time.time()  # Stop de timer
    print("[*] {} (mogelijk oplossingen gevonden in {}s)".format(mQueue.qsize(), time_stop - time_start))
    pq = mQueue.get(block=False)  # Haal het gevonden priemgetal op

    # print("Priemgetal gevonden in {}s,\npq = {}".format(time_stop - time_start, pq))

    # Stop al de threads
    _STOP_THREADS = True  # Geef signaal door

    return pq


# Testen van algoritmes
def get_max_iter(max: int, min: int) -> int:
    """ Geeft het aantal nummers weer die moeten overlopen worden om een priemgetal te bereiken """
    return (max - min) // 2


def compare(p: int, q: int, pmax: int, qmax: int, pmin: int, qmin: int) -> None:
    """ Kijkt of p en q binnen de grenzen vallen ==> Testen van algoritme """
    print("p < pmax => {}".format(p < pmax))
    print("q < qmax => {}".format(q < qmax))
    print("p > pmin => {}".format(p > pmin))
    print("q > qmin => {}".format(q > qmin))


def get_time_needed_from_n(n: int, nbits: int, processor_ticks_per_uur: int) -> float:
    """ Geeft de maximale tijd in uren weer nodig om een priemgetal te berekenen """
    grens: int = pow(2, (15 * nbits) // 16)
    qmin = pow(2, (15 * nbits - 32) // 32)

    aantal_nummers = 0
    if n < grens:  # Dit pad zal nooit worden gebruikt omdat nmin nooit onder de grens zal liggen
        aantal_nummers = isqrt(n) - qmin
    else:
        aantal_nummers = pow(2, (15 * nbits) // 32) - qmin

    #return math.log(aantal_nummers, 2) - processor_ticks_per_uur
    return aantal_nummers // pow(2, processor_ticks_per_uur)


def init(n: int, nbits: int, aantal_threads: int = 1) -> int:
    """ Voert bovenstaande functies uit en zoekt naar een priemgetal """
    pq1 = get_pq_max_min(nbits)
    pq_from_n = get_pq_max_min_from_n(n, *pq1)

    final = get_final_pq_max_min(n, *pq1, *pq_from_n)

    result_pq = 0  # uiteindelijke uitkomst
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
    init(43931, 16, 3)  # p = 223; q = 197
