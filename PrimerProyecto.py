import math

class tableRow():
    def __init__(self):
        self.li = 0
        self.ls = 0
        self.fi = 0
        self.fir = 0
        self.firP = 0
        self.fa = 0
        self.far = 0
        self.farP = 0
        self.xi = 0
        self.fixi = 0
        self.fixi2 = 0

# dic = {
#     'li': 0,
#     'ls': 0,
#     'fi': 0,
#     'fir': 0,
#     'firP': 0,
#     'fa': 0,
#     'far': 0,
#     'farP': 0,
#     'xi': 0,
#     'fixi': 0,
#     'fixi2': 0

# }

testData =  [
                30,	46,	71,	66,	34,	95,	50,	69,	31,	55,	42,	65,	75,	77,	32,	87,	75,	89,	31,	54,
                63,	95,	35,	86,	80,	47,	90,	82,	53,	58,	48,	66,	78,	78, 38,	82,	75,	31,	80,	79,
                48,	94,	77,	64,	38,	95,	46,	70,	30,	60,	50,	68,	34,	73,	98,	98,	33,	84,	98,	92,
                65,	44,	76,	96,	97,	37,	81,	85,	48,	61,	52, 47,	77,	50,	50,	49,	96,	97,	82,	49,
                33,	78,	70,	48,	96,	82,	40,	68,	34,	62,	54,	58,	54,	70,	35,	69,	98,	30,	88,	94,
                35,	51,	46,	92,	37,	38,	80,	54,	40,	39,	38,	54,	77,	62,	90,	39,	55,	50,	67,	31,
                68,	42,	48,	62,	40,	56,	94,	66,	39,	45,	33,	59,	78,	64,	50,	35,	45,	56,	69,	80,
                69,	39,	78,	65,	42,	55,	95,	78,	45,	56,	36,	58,	80,	68, 56,	36,	54,	65,	96,	76,
                74,	67,	93,	66,	44,	55,	82,	72,	54,	80,	94,	48,	34,	73,	61,	46,	76,	82,	64,	64,
                89,	89,	75,	66,	45,	59,	71,	89,	76,	74,	86,	56,	44,	91,	62,	78,	86,	83,	76,	68
            ]



table = []


def tableClasses(xMin, k, a):
     
    for i in range (k):
        table.append(tableRow())

    liCount = 0

    for row in table:
        row.li = xMin + (a * liCount)
        row.ls = row.li + a
        liCount += 1

def absoluteFrequency(data):
    for row in table:
        for value in data:
            if row.li <= value < row.ls:
                row.fi += 1

def acumulatedFrequency(k):
    for i in range(k):
        fa = 0
        if i-1 < 0 or i-1 > k:
            fa = 0 
        else: 
            fa = table[i-1].fa
        table[i].fa = fa + table[i].fi

def absFreRelative(n):
    for row in table:
        row.fir = row.fi / n

def absFreRelPercentage():
    for row in table:
        row.firP = row.fir * 100

def acumFreRelative(n):
    for row in table:
        row.far = row.fa / n

def acumFreRelPercentage():
    for row in table:
        row.farP = row.far * 100

def calcMiddlePoints():
    for row in table:
        row.xi = (row.li + row.ls) / 2

def calcFiXi():
    for row in table:
        row.fixi = row.fi * row.xi

def calcFiXi2():
    for row in table:
        row.fixi2 = row.fixi * row.xi

def arithAverage(n):
    acum = 0
    for row in table:
        acum += row.fixi
    x = acum / n
    return x

def median(n, a):
    temp = n/2
    index = 0
    for i, row in enumerate(table):
        if row.fa >= temp:
            index = i
            break
    li = table[index].li
    fi = table[index].fi
    Fi = (index < 0) if 0 else table[index-1].fa
    return li + (((temp - Fi) / fi) * a)

def modas(n, a):
    moda = 0
    # index = []
    result = []
    for row in table:
        if row.fi > moda:
            moda = row.fi

    for i, row in enumerate(table):
        if row.fi == moda:
            d1 = row.fi - ((i < 0) if 0 else table[i-1].fi)
            d2 = row.fi - ((i > len(table)) if 0 else table[i+1].fi)
            result.append(row.li + ((d1 / (d1 + d2)) * a))
    return result
    
def percentil(n, a, k, div):
    temp = (n * k) / div
    pk = 0
    for i, row in enumerate(table):
        if temp <= row.fa:
            Fi = 0
            if (i - 1) > 0:
                Fi =  table[i-1].fa
            pk = row.li + (((temp - Fi) / row.fi) * a)
            break
    return pk

def interquartileRange(n, a):
    return percentil(n, a, 3, 4) - percentil(n, a, 1, 4)

#def variance():



def fillTable(data):
    n = len(data)
    xMax = max(data)
    xMin = min(data)
    #r = xMax - xMin + 1
    r = xMax - xMin
    k = round(1 + 3.3*math.log10(n))
    a = round(r / k)
    tableClasses(xMin, k, a)
    absoluteFrequency(data)
    acumulatedFrequency(k)
    absFreRelative(n)
    absFreRelPercentage()
    acumFreRelative(n)
    acumFreRelPercentage()
    calcMiddlePoints()
    calcFiXi()
    calcFiXi2()
    x = arithAverage(n)
    me = median(n, a)
    mo = modas(n, a)
    cola = []
    # for moda in mo: cola.append(simetria()) 

    for row in table:
        print(str(row.li) + "-" + str(row.ls) + "  " + str(row.fi) + "  " + str(row.fa) + " " + str(row.xi), str(row.fixi))
    print(" media aritmetica: " +  str(x))
    print(" mediana: " +  str(me))
    print(" Moda: " + str(mo[0]))
    
    pk = int(input("Percentil a Calcular: "))
    print("Percentil " + str(pk) + ": " + str(percentil(n, a, pk, 100)))

    q = int(input("Quartil a Calcular: "))
    print("Quartil " + str(q) + ": " + str(percentil(n, a, q, 4)))

    dk = int(input("Decil a Calcular: "))
    print("Decil " + str(dk) + ": " + str(percentil(n, a, dk, 10)))

    print("Rango Intercuartil: " + str(interquartileRange(n, a)))









a = True
while(a):
    print(" ")
    print("=============Menu=============")
    print("Options")
    print("(1) Normal Pending")
    print("(2) ")
    print("(3) ")
    print("(4) ")
    print("(5) Exit")
    ans = input()
    if int(ans) == 5:
        print("GoodBy-e")
        a = False
    else:
        fillTable(testData)
