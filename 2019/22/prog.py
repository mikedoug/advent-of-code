


# Deal into new stack == reversed()
# cut N cards = slice(N:) + slice(0:N) -- cut -N cards = slice(-N:) + slice(0:-N)
# deal w/ inc 3: 04815926A37B

def deal_into_new_stack(cards):
    return list(reversed(cards))

def cut_n_cards(cards, n):
    return cards[n:] + cards[0:n]

def deal_with_increment(cards, inc):
    newdeck = [0] * len(cards)

    x = 0
    for i in range(len(cards)):
        newdeck[x] = cards[i]
        x += inc
        if x >= len(cards):
            x = x % len(cards)
    
    return newdeck

import re

with open("input2.txt", "r") as f:
    lines = f.readlines()

deck = list(range(10))
matcher = re.compile(r'(cut|deal with increment|deal into new stack) ?(-?\d*)')
for line in lines:
    line = line.rstrip()
    m = matcher.match(line)
    if m[1] == 'deal with increment':
        deck = deal_with_increment(deck, int(m[2]))
    elif m[1] == 'cut':
        deck = cut_n_cards(deck, int(m[2]))
    elif m[1] == 'deal into new stack':
        deck = deal_into_new_stack(deck)
    else:
        print(f'Invalid command: {line}') 
    
print(deck)
for i, card in enumerate(deck):
    if card == 2019:
        print (i)
        break


# position = 5
# value = 5
# matcher = re.compile(r'(cut|deal with increment|deal into new stack) ?(-?\d*)')
# for line in lines:
#     line = line.rstrip()
#     m = matcher.match(line)
#     if m[1] == 'deal with increment':
#         deck = deal_with_increment(deck, int(m[2]))
#     elif m[1] == 'cut':
#         value += int(m[2])
#     elif m[1] == 'deal into new stack':
#         deck = deal_into_new_stack(deck)
#     else:
#         print(f'Invalid command: {line}')
