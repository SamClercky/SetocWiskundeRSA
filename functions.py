# Stelling van Euler l^p (mod m)
def powmod(l,p,m):
    return pow(l,p) % m

# A simple Python3 program  
# to calculate Euler's  
# Totient Function 
  
# Function to return 
# gcd of a and b 
def gcd(a, b): 
  
    if (a == 0): 
        return b 
    return gcd(b % a, a) 
  
# A simple method to evaluate 
# Euler Totient Function 
def phi(n): 
  
    result = 1
    for i in range(2, n): 
        if (gcd(i, n) == 1): 
            result+=1
    return result

# phi uit 2 priemgetallen
def phi2(p, q):
    return (p - 1)*(q - 1)

def findJ(k, phipq):
    for i in range(phipq):
        if (k*i % phipq) == 1:
            return i