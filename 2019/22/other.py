inp = open("input.txt").readlines()

N = 119315717514047
#N=10007

# (i * a + b)%N = pos of card i
cards = (1, 0)

def rev(cards):
  # x -> N-1 - x = -1 - x = -(x+1)
  return ((-cards[0])%N, (-cards[1]-1)%N)

def cut(cards, n):
  return (cards[0], (cards[1]-n)%N)

def deal(cards, n):
  return ((cards[0]*n)%N, (cards[1]*n)%N)


for line in inp:
  if line.startswith("deal i"):
    cards = rev(cards)
  elif line.startswith("cut"):
    cards = cut(cards, int(line[3:].strip()))
  elif line.startswith("deal w"):
    cards = deal(cards, int(line[len("deal with increment"):].strip()))
  else:
    print ("Unknown: " + line)


#repeat a bunch

rep = 101741582076661

#i -> i*a + b
# rep n times
#i*a^2 + ab + b
#i*a^3 + a^2b + ab + b
#i*a^n + b*(sum j=0..n-1 a^j)
#i*a^n + b*(a^n-1)/(a-1)

# copied from stackoverflow
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
# end stackoverflow part

def mod_pow(a, b, n):
  if b == 1:
    return a
  if b%2 == 0:
    return mod_pow(a, b//2, n)**2 % n
  if b%2 == 1:
    return a*mod_pow(a, b-1, n) % n

a, b = cards
an = mod_pow(a, rep, N)

A, B = an, b*(an-1) * mod_inv(a-1, N)
print((2019 * A + B) % N)

# want card in pos 2020
print((2020 - B)*mod_inv(A, N) % N)