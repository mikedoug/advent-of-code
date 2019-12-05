def repeatTest(x):
    for i in range(1, len(x)):
        if x[i] == x[i-1]:
            return True
    return False

def repeatsTwiceTest(x):
    for i in range(1, len(x)):
        if x[i] == x[i-1] and \
            (i == len(x)-1 or x[i+1] != x[i]) and \
            (i == 1 or x[i-2] != x[i]):
                return True
    return False
    
def ascendingTest(x):
    for i in range(1, len(x)):
        if x[i] < x[i-1]:
            return False
    return True

count = 0
for x in range(254032, 789860):
    digits = list(map(lambda x: int(x), str(x)))
    
    if repeatsTwiceTest(digits) and ascendingTest(digits):
        count += 1

print(count)