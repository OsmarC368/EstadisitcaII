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


def findXmax(data):
    xMax = 0
    for value in data:
        if value > xMax:
            xMax = value
    return xMax

def findXmin(data):
    xMin = 9999999999999999 * 9999999999999
    for value in data:
        if value < xMin:
            xMin = value
    return xMin

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



def fillTable(data):
    n = len(data)
    xMax = findXmax(data)
    xMin = findXmin(data)
    r = xMax - xMin + 1
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

    for row in table:
        print(str(row.li) + "-" + str(row.ls) + "  " + str(row.fi) + "  " + str(row.fa) + " " + str(row.xi), str(row.fixi))
    print(" media aritmetica: " +  str(x))





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