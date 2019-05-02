import rsa
from algo2 import init

# Declareer alle globale variabelen voor tests
nbits = 64
(pubkey, privkey) = rsa.newkeys(nbits)

n = pubkey.n
p = privkey.p
q = privkey.q

def reset(new_nbits):
    """ Reset van alle globale variabelen volgens nbits """
    global nbits, pubkey, privkey, n, p, q
    nbits = new_nbits

    (pubkey, privkey) = rsa.newkeys(nbits)

    n = pubkey.n
    p = privkey.p
    q = privkey.q

def start_all(aantal_threads = 3):
    """ Start het zoekprogramma """
    init(n, nbits, aantal_threads)
