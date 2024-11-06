import math
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import cutie
import numpy as np

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

testData = [
                30,	46,	71,	66,	34,	95,	50,	69,	31,	55,	42,	65,	75,	77,	32,	87,	75,	89,	31,	54,
                63,	95,	35,	86,	80,	47,	90,	82,	53,	58,	48,	66,	78,	78, 38,	82,	75,	31,	80,	79,
                48,	94,	77,	64,	38,	95,	46,	70,	30,	60,	50,	68,	34,	73,	98,	98,	33,	84,	98,	92,
                65,	44,	76,	96,	97,	37,	81,	85,	48,	61,	52, 47,	77,	50,	50,	49,	96,	97,	82,	49,
                33,	78,	70,	48,	96,	82,	40,	68,	34,	62,	54,	58,	54,	70,	35,	69,	98,	30,	88,	94,
                35,	51,	46,	92,	37,	38,	80,	54,	40,	39,	38,	54,	77,	62,	90,	39,	55,	50,	67,	31,
                68,	42,	48,	62,	40,	56,	94,	66,	39,	45,	33,	59,	78,	64,	50,	35,	45,	56,	69,	80,
                69,	39,	78,	65,	42,	55,	95,	78,	45,	56,	36,	58,	80,	68, 56,	36,	54,	65,	96,	76,
                74,	67,	93,	66,	44,	55,	82,	72,	54,	80,	94,	48,	34,	73,	61,	46,	76,	82,	64,	64,
                89,	89,	75,	66,	45,	59,	71,	89,	76,	74,	86,	56,	44,	91,	62,	79, 89, 87, 79, 69,
                35, 35, 35, 35, 35
            ]



def tableClasses(table, xMin, k, a):
     
    for i in range (k):
        table.append(tableRow())

    liCount = 0

    for row in table:
        row.li = xMin + (a * liCount)
        row.ls = row.li + a
        liCount += 1

def absoluteFrequency(table, data):
    for row in table:
        for value in data:
            if row.li <= value < row.ls:
                row.fi += 1

def acumulatedFrequency(table, k):
    for i in range(k):
        fa = 0 if (i-1 < 0 or i-1 > k) else table[i-1].fa
        if i-1 < 0 or i-1 > k:
            fa = 0 
        else: 
            fa = table[i-1].fa
        table[i].fa = fa + table[i].fi

def absFreRelative(table, n):
    for row in table:
        row.fir = row.fi / n

def absFreRelPercentage(table):
    for row in table:
        row.firP = row.fir * 100

def acumFreRelative(table, n):
    for row in table:
        row.far = row.fa / n

def acumFreRelPercentage(table):
    for row in table:
        row.farP = row.far * 100

def calcMiddlePoints(table):
    for row in table:
        row.xi = (row.li + row.ls) / 2

def calcFiXi(table):
    for row in table:
        row.fixi = row.fi * row.xi

def calcFiXi2(table):
    for row in table:
        row.fixi2 = row.fixi * row.xi

def arithAverage(table, n):
    sumFixi = sum(row.fixi for row in table)
    x = sumFixi / n
    return x

def median(table, n, a):
    temp = n/2
    index = 0
    for i, row in enumerate(table):
        if row.fa >= temp:
            index = i
            break
    li = table[index].li
    fi = table[index].fi
    Fi = 0 if(index < 0) else table[index-1].fa
    return li + (((temp - Fi) / fi) * a)

def modas(table, a):

    moda = max(row.fi for row in table)
    result = []

    for i, row in enumerate(table):
        if row.fi == moda:
            d1 = row.fi - (0 if (i <= 0) else table[i-1].fi)
            d2 = row.fi - (0 if (i >= (len(table) - 1)) else table[i+1].fi)
            if d1 == 0 and d2 == 0:
                print("Moda #" + str(len(result) + 1) + ": Error Division por 0 por lo que se usara 1 en d1/(d1+d2)")
                result.append(row.li + a)
            else:
                result.append(row.li + ((d1 / (d1 + d2)) * a))
    return result
    
def percentil(table, n, a, k, div):
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

def interquartileRange(table, n, a):
    return percentil(table, n, a, 3, 4) - percentil(table, n, a, 1, 4)

def variance(table, n, x):
    sumFiXi2 = sum(row.fixi2 for row in table)
    return (sumFiXi2 / n) - math.pow(x, 2)

def curtosis(table, n, a):
    return ((percentil(table, n, a, 75, 100) - percentil(table, n, a, 25, 100)) / (percentil(table, n, a, 90, 100) - percentil(table, n, a, 10, 100))) * 0.5

def showGraph(data, bins, title):
    plt.hist(data, bins=bins, edgecolor='yellow', color='red')
    plt.title(f"{title} Histogram \n", fontweight='bold')
    plt.show()


def fillTable(data, title):
    table = []
    ans = "0"
    n = len(data)
    xMax = max(data)
    xMin = min(data)
    r = xMax - xMin
    k = round(1 + 3.3*math.log10(n))
    a = round(r / k)
    tableClasses(table, xMin, k, a)
    absoluteFrequency(table, data)
    acumulatedFrequency(table, k)
    absFreRelative(table, n)
    absFreRelPercentage(table)
    acumFreRelative(table, n)
    acumFreRelPercentage(table)
    calcMiddlePoints(table)
    calcFiXi(table)
    calcFiXi2(table)
    x = arithAverage(table, n)
    me = median(table, n, a)
    mo = modas(table, a)
    s2 = variance(table, n, x)
    s = math.sqrt(s2)
    cv =  s / x
    As = (3 * (x - me)) / s
    c = curtosis(table, n, a)
    options = [
                '- Frequency table', '- Table Metrics', '- Arithm Mean', '- Median', '- mode', '- Calcualte Percentile',
                '- Calculate Decile', '- Calculate Quantile', '- Interquartile Range', '- Variance', '- Standard Deviation',
                '- Coefficient of Variation', '- Asymmetry Index', '- Kurtosis', '- Show Hist Graph','<- Back'
            ]
    while(ans != "16"):
        print(" ")
        print(f"============= {title} FREQUENCY TABLE MENU =============")
        print("/----------Options----------/")
        optionIndex = cutie.select(options)
        ans = str(optionIndex + 1)
        if ans == "1":
            data = []
            print("\n/------------------------------------------------------------------------------------------/")
            for row in table:
                rowData = []
                rowData.append(f'{row.li} - {row.ls}')
                rowData.append(row.fi)
                rowData.append(row.fa)
                rowData.append(format(row.fir, '.4f'))
                rowData.append(format(row.firP, '.2f'))
                rowData.append(format(row.far, '.4f'))
                rowData.append(format(row.farP, '.2f'))
                rowData.append(format(row.xi, '.2f'))
                rowData.append(format(row.fixi, '.2f'))
                rowData.append(format(row.fixi2, '.2f'))
                data.append(rowData)
            print(tabulate(data, headers=['Clases', 'fi', 'fa', 'fir', 'fir%', 'far', 'far%', 'xi', 'fixi', 'fixi2'], tablefmt='fancy_grid'))
            # print(tabulate(data, headers=['Clases', 'fi', 'fa', 'fir', 'fir%', 'far', 'far%', 'xi', 'fixi', 'fixi2'], tablefmt='github'))
            print("/------------------------------------------------------------------------------------------/")
                            
        elif ans == "2":
            print("\n/---------------------------------/")
            print(f"Amount of Data: {n}")
            print(f"Number of Classes: {k}")
            print(f"Amplitude: {a}")
            print(f"X Min: {xMin}")
            print(f"X Max: {xMax}")
            print(f"Range: {r}")
            print("/---------------------------------/")

        elif ans == "3":
            print("\n/---------------------------------/")
            print(f"Arithm Mean: {format(x, '.2f')}")
            print("/---------------------------------/")

        elif ans == "4":
            print("\n/---------------------------------/")
            print(f"Median: {format(me, '.2f')}")
            print("/---------------------------------/")

        elif ans == "5":
            print("\n/---------------------------------/")
            for i, mode in enumerate(mo):
                print(f"Mode #{i+1}: {format(mode, '.2f')}")
            print("/---------------------------------/")

        elif ans == "6":
            print("\n/---------------------------------/")
            try: pk = int(input("Percentile to Calculate: "))
            except: 
                print("Error: Not a Integer Value") 
                break
            if 0 < pk <= 100:
                print(f"Percentil {pk}: {str(format(percentil(table, n, a, pk, 100), '.2f'))}")
            else:
                print("Error: Out of Range")
            print("/---------------------------------/")
            

        elif ans == "7":
            print("\n/---------------------------------/")
            try: dk = int(input("Decile to Calculate: "))
            except: 
                print("Error: Not a Integer Value") 
                break
            if 0 < dk <= 10:
                print(f"Decile {dk}: {format(percentil(table, n, a, dk, 10), '.2f')}")
            else:
                print("Error: Out of Range")
            print("/---------------------------------/")

        elif ans == "8":
            print("\n/---------------------------------/")
            try: qk = int(input("Quartile to Calculate: "))
            except: 
                print("Error: Not a Integer Value") 
                break
            if 0 < qk < 4:
                print(f"Quartile {qk}: {format(percentil(table, n, a, qk, 4), '.2f')}")
            else:
                print("Error: Out of Range")
            print("/---------------------------------/")

        elif ans == "9":
            print("\n/---------------------------------/")
            print(f"Interquartile Range: {format(interquartileRange(table, n, a), '.2f')}")
            print("/---------------------------------/")

        elif ans == "10":
            print("\n/---------------------------------/")
            print(f"Variance: {format(s2, '.2f')}")
            print("/---------------------------------/")

        elif ans == "11":
            print("\n/---------------------------------/")
            print(f"Standard Deviation: {format(s, '.2f')}")
            print("/---------------------------------/")

        elif ans == "12":
            print("\n/---------------------------------/")
            print(f"Coefficient of Variation: {format((cv * 100), '.2f')}")
            print("/---------------------------------/")

        elif ans == "13":
            print("\n/---------------------------------/")
            print(F"Asymmetry Index: {format(As, '.4f')}")
            print("/---------------------------------/")

        elif ans == "14":
            print("\n/---------------------------------/")
            print(f"Kurtosis: {format(c, '.4f')}")   
            print("/---------------------------------/")

        elif ans == "15":
            bins = []
            for row in table:
                bins.append(row.li)
            plt.close('all')
            showGraph(data, bins, title)

def sexGraph():
    plt.close('all')
    male = sex.count(0)
    female = sex.count(1)
    labels = ['Male','Female']
    sexData = np.array([male, female])
    colors = ["#52a4ec", "#ea74f3"]
    plt.pie(sexData, labels=labels, colors=colors)
    plt.title("Sex Pie Graphic")
    plt.legend()
    plt.show()

def marriedGraph():
    plt.close('all')
    single = married.count(0)
    marriedC = married.count(1)
    labels = ['Single','Married']
    sexData = np.array([single, marriedC])
    colors = ["#52a4ec", "#ea74f3"]
    plt.pie(sexData, labels=labels, colors=colors)
    plt.title("Married Pie Graphic")
    plt.legend()
    plt.show()

def mainMenu():
    
    
    ans = 0
    options = [
        '- Sex', '- Age', '- Married', '- Income', '- Hours WK', '- Race', '- usCitizen', '- Health Insurance', '- languaje', '- Classic Data', '- Exit'

    ]
    while(ans < 11):
        print("\n================================================================")
        print("========================== MAIN MENU ===========================")
        print("================================================================")
        optChoice = cutie.select(options)
        ans = optChoice + 1
        
        if ans == 1:
            sexGraph()
        elif ans == 2:
            fillTable(age, "AGE")
        elif ans == 3:
            marriedGraph()
        elif ans == 4:
            fillTable(income, "INCOME")
        elif ans == 5:
            fillTable(hoursWK, "HOURS WORKING")
        elif ans == 6:
            print("Work in Progress")
        elif ans == 7:
            print("Work in Progress")
        elif ans == 8:
            print("Work in Progress")
        elif ans == 9:
            print("Work in Progress")
        elif ans == 10:
            fillTable(testData, "OLD DATA")
        elif ans == 11:
            print("Go0dbyE HUmAn $%&/%##")




sex = []
age = []
married = []
income = []
hoursWK = []
race = []
usCitizen = []
healthInsurance = []
language = []

if __name__ == "__main__":
    with open("Datosproyecto2024.csv", newline="") as dataBase:
        spamreader = csv.reader(dataBase)
        i = 0
        for row in spamreader:
            if i > 0:
                # data = row[0].split(",")
                sex.append(int(row[0]))
                age.append(int(row[1]))
                married.append(int(row[2]))
                income.append(float(row[3]))
                hoursWK.append(float(row[4]))
                race.append(row[5])
                usCitizen.append(int(row[6]))
                healthInsurance.append(float(row[7]))
                language.append(int(row[8]))
            i = 1
    mainMenu()

