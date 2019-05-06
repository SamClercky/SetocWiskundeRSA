import rsa
import algo2 as a

# Declareer alle globale variabelen voor tests
nbits = 64
(pubkey, privkey) = rsa.newkeys(nbits)

n = pubkey.n
p = privkey.p
q = privkey.q

pq1 = a.get_pq_max_min(nbits)
pq_from_n = a.get_pq_max_min_from_n(n,*pq1)
final = a.get_final_pq_max_min(n, *pq1, *pq_from_n)

def reset(new_nbits):
    """ Reset van alle globale variabelen volgens nbits """
    global nbits, pubkey, privkey, n, p, q, pq1, pq_from_n, final
    nbits = new_nbits

    (pubkey, privkey) = rsa.newkeys(nbits)

    n = pubkey.n
    p = privkey.p
    q = privkey.q

    pq1 = a.get_pq_max_min(nbits)
    pq_from_n = a.get_pq_max_min_from_n(n,*pq1)
    final = a.get_final_pq_max_min(n, *pq1, *pq_from_n)

def start_all(aantal_threads = 3):
    """ Start het zoekprogramma """
    a.init(n, nbits, aantal_threads)
