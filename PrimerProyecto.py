import math
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import cutie
import numpy as np
from scipy.stats import norm
import random
import seaborn as sns

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
    Fi = 0 if(index == 0) else table[index-1].fa
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
                result.append(format((row.li + ((d1 / (d1 + d2)) * a)), '.2f'))
    return result
    
def percentil(table, n, a, k, div):
    temp = (n * k) / div
    pk = 0
    for i, row in enumerate(table):
        if temp <= row.fa:
            # Fi = 0 if i-1 <= 0 else table[i-1]
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
    # plt.hist(data, bins=bins, edgecolor='yellow', color='red')
    # plt.plot(bins, '--', color='black')
    sns.histplot(data, bins=bins, kde=True, edgecolor='yellow', color='red')
    plt.title(f"{title} Histogram \n", fontweight='bold')
    plt.show()

def getDispersionType(c):
    if c == 0:
        return 'Mesocurtica'
    elif c > 0:
        return 'Platicurtica'
    else:
        return 'Leptocurtica'

def fillTable(data, title, ansS):
    table = []
    ans = ansS
    n = len(data)
    xMax = max(data)
    xMin = min(data)
    r = (xMax - xMin) + 1
    k = round(1 + 3.3*math.log10(n))
    # a = round(r / k) + 1
    a = math.ceil(r / k)
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
            tableData = []
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
                tableData.append(rowData)
            print(tabulate(tableData, headers=['Clases', 'fi', 'fa', 'fir', 'fir%', 'far', 'far%', 'xi', 'fixi', 'fixi2'], tablefmt='fancy_grid'))
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
                print(f"Mode #{i+1}: {mode}")
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
            if 0 < qk <= 4:
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
            print(f"{getDispersionType(c)}")
            print("/---------------------------------/")

        elif ans == "15":
            bins = []
            for row in table:
                bins.append(row.li)
            plt.close('all')
            showGraph(data, bins, title)

    return [percentil(table, n, a, 1, 4), percentil(table, n, a, 2, 4), percentil(table, n, a, 3, 4), percentil(table, n, a, 4, 4),
            x, mo, me,
            s2, s, cv*100, interquartileRange(table, n, a),
            c, As,
            n]

def sexGraph():
    plt.close('all')
    male = sex.count(1)
    female = sex.count(0)
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
    colors = ["#cec284", "#a52a2a"]
    plt.pie(sexData, labels=labels, colors=colors)
    plt.title("Married Pie Graphic")
    plt.legend()
    plt.show()


def raceGraph():
    plt.close('all')
    white =  race.count('white')
    black =  race.count('black')
    asian =  race.count('asian')
    other =  race.count('other')
    labels = ['White', 'Black', 'Asian', 'Other']
    raceData = np.array([white, black, asian, other])
    colors = ["gray", "black", "yellow", "purple"]
    plt.pie(raceData, labels=labels, colors=colors)
    plt.title("Race Pie Graphic")
    plt.legend()
    plt.show()

def usCitizenGraph():
    plt.close('all')
    citizen =  usCitizen.count(1)
    notCitizen =  usCitizen.count(0)
    labels = ['Citizen', 'Not Citizen']
    citizenData = np.array([citizen, notCitizen])
    colors = ["blue", "black"]
    plt.pie(citizenData, labels=labels, colors=colors)
    plt.title("US Citizenship Pie Graphic")
    plt.legend()
    plt.show()

def healthInsurenceGraph():
    plt.close('all')
    yes =  healthInsurance.count(1)
    no =  healthInsurance.count(0)
    labels = ['Have Health Insurance', 'No Health Insurance']
    heInData = np.array([yes, no])
    colors = ["#5ABA4A", "#F7CC3B"]
    plt.pie(heInData, labels=labels, colors=colors)
    plt.title("Health Insurence Pie Graphic")
    plt.legend()
    plt.show()

def languageGraph():
    plt.close('all')
    yes =  language.count(1)
    no =  language.count(0)
    labels = ['English Spoken at Home', 'Other']
    heInData = np.array([yes, no])
    colors = ["#efab0f", "#6814a2"]
    plt.pie(heInData, labels=labels, colors=colors)
    plt.title("Language Pie Graphic")
    plt.legend()
    plt.show()

def getTableDataInfo(data):
    tableData = []
    tableData.append(['Position', ''])
    tableData.append(['Q1', format(data[0], '.2f')])
    tableData.append(['Q2', format(data[1], '.2f')])
    tableData.append(['Q3', format(data[2], '.2f')])
    tableData.append(['Q4', format(data[3], '.2f')])
    tableData.append(['Central', ''])
    tableData.append(['Arithm Media', format(data[4], '.2f')])
    tableData.append(['Mode', data[5]])
    tableData.append(['Median', format(data[6], '.2f')])
    tableData.append(['Variabilability', ''])
    tableData.append(['Variance', format(data[7], '.2f')])
    tableData.append(['Standard Diviation', format(data[8], '.2f')])
    tableData.append(['CV', format(data[9], '.2f')])
    tableData.append(['IQR', format(data[10], '.2f')])
    tableData.append(['Form', ''])
    tableData.append(['Kurtosis', format(data[11], '.4f')])
    tableData.append(['As', format(data[12], '.4f')])
    return tableData

def showFaseI():
    ageData = fillTable(age, "AGE", "16")
    incomeData = fillTable(income, "INCOME", "16")
    hoursWKData = fillTable(hoursWK, "HOURS WORKING", "16")

    ageTableData = getTableDataInfo(ageData)
    incomeTableData = getTableDataInfo(incomeData)
    hoursWKTableData = getTableDataInfo(hoursWKData)
    print("\n------------------------------------------------------------")
    print("-------------------------- FASE I --------------------------")
    print("------------------------------------------------------------")
    print("\n/------------------------------------------------------------------------------------------/")
    print('========== AGE ==========')
    print(tabulate(ageTableData, headers=['Variable: Age', ''], tablefmt='fancy_grid'))
    print("/------------------------------------------------------------------------------------------/")
    print('========== INCOME ==========')
    print(tabulate(incomeTableData, headers=['Variable: Income ', ''], tablefmt='fancy_grid'))
    print("/------------------------------------------------------------------------------------------/")
    print('========== HOURS WK ==========')
    print(tabulate(hoursWKTableData, headers=['Variable: Hours WK ', ''], tablefmt='fancy_grid'))
    print("/------------------------------------------------------------------------------------------/")


def raceSexTable():
    srTableData = []

    femAsian = 0
    femBlack = 0
    femWhite = 0
    femOther = 0
    femTotal = 0

    maleAsian = 0
    maleBlack = 0
    maleWhite = 0
    maleOther = 0
    maleTotal = 0

    for i in range(len(sex)):
        femAsian += 1 if sex[i] == 0 and race[i] == 'asian' else 0
        femBlack += 1 if sex[i] == 0 and race[i] == 'black' else 0
        femWhite += 1 if sex[i] == 0 and race[i] == 'white' else 0
        femOther += 1 if sex[i] == 0 and race[i] == 'other' else 0
        femTotal += 1 if sex[i] == 0 else 0

        maleAsian += 1 if sex[i] == 1 and race[i] == 'asian' else 0
        maleBlack += 1 if sex[i] == 1 and race[i] == 'black' else 0
        maleWhite += 1 if sex[i] == 1 and race[i] == 'white' else 0
        maleOther += 1 if sex[i] == 1 and race[i] == 'other' else 0
        maleTotal += 1 if sex[i] == 1 else 0
    
    srTableData.append(['sex'])
    srTableData.append(['F', femAsian, femBlack, femWhite, femOther, femTotal])
    srTableData.append(['M', maleAsian, maleBlack, maleWhite, maleOther, maleTotal])
    srTableData.append(['Total', (femAsian + maleAsian), (femBlack + maleBlack), (femWhite + maleWhite), (femOther + maleOther), (femTotal + maleTotal)])
    
    print(tabulate(srTableData, headers=['Race', 'Asian', 'Black', 'White', 'Other', 'Total'], tablefmt='fancy_grid'))

    objList = [
                {'name': 'Female Asian', 'value':femAsian}, {'name':'Female Black', 'value':femBlack}, {'name': 'Female White', 'value': femWhite}, {'name':'Female Other', 'value':femOther}, 
                {'name': 'Male Asian', 'value': maleAsian}, {'name': 'Male Black', 'value': maleBlack}, {'name': 'Male White', 'value': maleWhite}, {'name': 'Male Other', 'value': maleOther}
            ]

    maxObj = max(objList, key=lambda i: i['value'])
    print(f"\nBiggest Percentage:  {maxObj['name']} {(maxObj['value'] / len(sex) )* 100}%\n")



def ageHoursWKTable():
    ahTableData = [['Age']]
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])
    ahTableData.append(['', 0, 0, 0, 0])

    for i in range(len(age)):
        ahTableData[1][0] = '14-24'
        ahTableData[1][1] += 1 if 14 <= age[i] <= 24 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[1][2] += 1 if 14 <= age[i] <= 24 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[1][3] += 1 if 14 <= age[i] <= 24 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[1][4] += 1 if 14 <= age[i] <= 24 and hoursWK[i] > 59 else 0

        ahTableData[2][0] = '25-34'
        ahTableData[2][1] += 1 if 25 <= age[i] <= 34 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[2][2] += 1 if 25 <= age[i] <= 34 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[2][3] += 1 if 25 <= age[i] <= 34 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[2][4] += 1 if 25 <= age[i] <= 34 and hoursWK[i] > 59 else 0

        ahTableData[3][0] = '35-44'
        ahTableData[3][1] += 1 if 35 <= age[i] <= 44 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[3][2] += 1 if 35 <= age[i] <= 44 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[3][3] += 1 if 35 <= age[i] <= 44 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[3][4] += 1 if 35 <= age[i] <= 44 and hoursWK[i] > 59 else 0

        ahTableData[4][0] = '45-54'
        ahTableData[4][1] += 1 if 45 <= age[i] <= 54 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[4][2] += 1 if 45 <= age[i] <= 54 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[4][3] += 1 if 45 <= age[i] <= 54 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[4][4] += 1 if 45 <= age[i] <= 54 and hoursWK[i] > 59 else 0

        ahTableData[5][0] = '55-64'
        ahTableData[5][1] += 1 if 55 <= age[i] <= 64 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[5][2] += 1 if 55 <= age[i] <= 64 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[5][3] += 1 if 55 <= age[i] <= 64 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[5][4] += 1 if 55 <= age[i] <= 64 and hoursWK[i] > 59 else 0

        ahTableData[6][0] = '65-74'
        ahTableData[6][1] += 1 if 65 <= age[i] <= 74 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[6][2] += 1 if 65 <= age[i] <= 74 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[6][3] += 1 if 65 <= age[i] <= 74 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[6][4] += 1 if 65 <= age[i] <= 74 and hoursWK[i] > 59 else 0

        ahTableData[7][0] = '75-84'
        ahTableData[7][1] += 1 if 75 <= age[i] <= 84 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[7][2] += 1 if 75 <= age[i] <= 84 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[7][3] += 1 if 75 <= age[i] <= 84 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[7][4] += 1 if 75 <= age[i] <= 84 and hoursWK[i] > 59 else 0

        ahTableData[8][0] = '85-94'
        ahTableData[8][1] += 1 if 85 <= age[i] <= 94 and 0 <= hoursWK[i] <= 19 else 0
        ahTableData[8][2] += 1 if 85 <= age[i] <= 94 and 20 <= hoursWK[i] <= 39 else 0
        ahTableData[8][3] += 1 if 85 <= age[i] <= 94 and 40 <= hoursWK[i] <= 59 else 0
        ahTableData[8][4] += 1 if 85 <= age[i] <= 94 and hoursWK[i] > 59 else 0

    print(tabulate(ahTableData, headers=['Hours', '0-19', '20-39', '40-59', 'More Hours'], tablefmt='fancy_grid'))

    objList = [
        {'name': 'Edad: 14-24 Horas: 0-19', 'value': ahTableData[1][1]}, {'name': 'Edad: 14-24 Horas: 20-39', 'value': ahTableData[1][2]}, {'name': 'Edad: 14-24 Horas: 40-59', 'value': ahTableData[1][3]}, {'name': 'Edad: 14-24 Horas: Mas Horas', 'value': ahTableData[1][4]},
        {'name': 'Edad: 25-34 Horas: 0-19', 'value': ahTableData[2][1]}, {'name': 'Edad: 25-34 Horas: 1-2', 'value': ahTableData[2][2]}, {'name': 'Edad: 25-34 Horas: 40-59', 'value': ahTableData[2][3]}, {'name': 'Edad: 25-34 Horas: Mas Horas', 'value': ahTableData[2][4]},
        {'name': 'Edad: 35-44 Horas: 0-19', 'value': ahTableData[3][1]}, {'name': 'Edad: 35-44 Horas: 1-2', 'value': ahTableData[3][2]}, {'name': 'Edad: 35-44 Horas: 40-59', 'value': ahTableData[3][3]}, {'name': 'Edad: 35-44 Horas: Mas Horas', 'value': ahTableData[3][4]},
        {'name': 'Edad: 45-54 Horas: 0-19', 'value': ahTableData[4][1]}, {'name': 'Edad: 45-54 Horas: 1-2', 'value': ahTableData[4][2]}, {'name': 'Edad: 45-54 Horas: 40-59', 'value': ahTableData[4][3]}, {'name': 'Edad: 45-54 Horas: Mas Horas', 'value': ahTableData[4][4]},
        {'name': 'Edad: 55-64 Horas: 0-19', 'value': ahTableData[5][1]}, {'name': 'Edad: 55-64 Horas: 20-39', 'value': ahTableData[5][2]}, {'name': 'Edad: 55-64 Horas: 40-59', 'value': ahTableData[5][3]}, {'name': 'Edad: 55-64 Horas: Mas Horas', 'value': ahTableData[5][4]},
        {'name': 'Edad: 65-74 Horas: 0-19', 'value': ahTableData[6][1]}, {'name': 'Edad: 65-74 Horas: 1-2', 'value': ahTableData[6][2]}, {'name': 'Edad: 65-74 Horas: 40-59', 'value': ahTableData[6][3]}, {'name': 'Edad: 65-74 Horas: Mas Horas', 'value': ahTableData[6][4]},
        {'name': 'Edad: 75-84 Horas: 0-19', 'value': ahTableData[7][1]}, {'name': 'Edad: 75-84 Horas: 1-2', 'value': ahTableData[7][2]}, {'name': 'Edad: 75-84 Horas: 40-59', 'value': ahTableData[7][3]}, {'name': 'Edad: 75-84 Horas: Mas Horas', 'value': ahTableData[7][4]},
        {'name': 'Edad: 85-94 Horas: 0-19', 'value': ahTableData[8][1]}, {'name': 'Edad: 85-94 Horas: 1-2', 'value': ahTableData[8][2]}, {'name': 'Edad: 85-94 Horas: 40-59', 'value': ahTableData[8][3]}, {'name': 'Edad: 85-94 Horas: Mas Horas', 'value': ahTableData[8][4]}
    ]

    maxObj = max(objList, key=lambda i: i['value'])
    print(f"\nBiggest Percentage:  {maxObj['name']} {(maxObj['value'] / len(age) )* 100}%\n")

def ansQuestions(x, op, data, interval):
    res = fillTable(data, "test", "16")
    x = x
    u = res[4]
    sigma = res[8]
    n = len(data)

    # z = (x - u) / (sigma/(math.sqrt(n)))
    z = (x - u) / sigma
    p = float(norm.cdf(z))


    if op == 0:
        return format(p * 100, '.2f')
    elif op == 1:
        return format((1 - p) * 100, '.2f')
    elif op == 2:
        z1 = (interval[0] - u) / sigma
        z2 = (interval[1] - u) / sigma
        p1 = float(norm.cdf(z1))
        p2 = float(norm.cdf(z2))
        return format((p2 - p1)* 100, '.2f')
    else:
        return 0


def incomeRandomTable():
    g1 = random.sample(income, k=500)
    g2 = random.sample(income, k=500)
    g3 = random.sample(income, k=400)

    g1Data = fillTable(g1, '', '16')
    g2Data = fillTable(g2, '', '16')
    g3Data = fillTable(g3, '', '16')

    tableData = []
    tableData.append(['G1', len(g1), g1Data[4], g1Data[8]])
    tableData.append(['G2', len(g2), g2Data[4], g2Data[8]])
    tableData.append(['G3', len(g3), g3Data[4], g3Data[8]])
    print(tabulate(tableData, headers=['', 'Number of Elements', 'Arithm Mean', 'Standard Deviation'], tablefmt='fancy_grid'))
    print('')
    print(f'1)En cuanto a la variable salario, seleccionar G1 y G2, contrastar si dichas poblaciones se comportan iguales. Justifique su respuesta, utilizando un nivel de significancia del 95%')
    print(f'\n{hipotesis(g1Data, g2Data, 1.65, 0)}')
    print('')
    print(f'2)Podemos decidir si se debería comparar G2 y G3. Si los salarios en ambos grupos no se diferencian entre sí, con un nivel de significancia del 99%.')
    print(f'\n{hipotesis(g2Data, g3Data, 2.33, 0)}')
    


def hipotesis(data1, data2, sig, op):
    zTab = sig
    sigmaX = math.sqrt((data1[8]**2 / data1[13]) + (data2[8]**2 / data2[13]))
    zCalc = (data1[4] - data2[4]) / sigmaX
    if op == 0:
        if (zTab * -1) <= zCalc <= zTab:
            return f'Debido a que -zTab < zCalc < zTab ({(zTab * -1)} < {format(zCalc, '.2f')} < {zTab}), Aceptamos Ho'
        elif zCalc > zTab:
            return f'Debido a que zCalc > zTab ({format(zCalc, '.2f')} > {zTab}), Rechazamos Ho y Aceptamos Ha'
        else:
            return f'Debido a que zCalc < -zTab ({(zTab * -1)} > {format(zCalc, '.2f')}), Rechazamos Ho y Aceptamos Ha'
    else:
        if zCalc < zTab:
            return f'Debido a que zCalc < zTab ({format(zCalc, '.2f')} < {zTab}), Aceptamos Ho'
        else:
            return f'Debido a que zCalc > zTab ({format(zCalc, '.2f')} > {zTab}), Rechazamos Ho y Aceptamos Ha'


def ageRandomTable():
    g1 = random.sample(age, k=300)
    g2 = random.sample(age, k=400)

    g1Data = fillTable(g1, '', '16')
    g2Data = fillTable(g2, '', '16')

    tableData = []
    tableData.append(['G1', len(g1), g1Data[4], g1Data[8]])
    tableData.append(['G2', len(g2), g2Data[4], g2Data[8]])
    print(tabulate(tableData, headers=['', 'Number of Elements', 'Arithm Mean', 'Standard Deviation'], tablefmt='fancy_grid'))
    print('')
    print('¿se puede contrastar que los dos grupos el primer grupo es mayor que el segundo? con un nivel de significancia 90%')
    print(f'\n{hipotesis(g1Data, g2Data, 1.29, 1)}')
    print('')


def showFaseII():
    print("\n-----------------------------------------------------------")
    print("-------------------------- FASE II ------------------------")
    print("-----------------------------------------------------------")
    print("\n/------------------------------------------------------------------------------------------/")
    print('========== PROBABILITY QUESTIONS ==========')
    print(f'Pregunta 1: Cual es la probabilidad de que el salario sea mayor que 44? {ansQuestions(44, 1, income, None)}%\n')
    print(f'Pregunta 2: Cual es la probabilidad de que el salario de una persona se encuentre entre 47 y 49? {ansQuestions(0, 2, income, [47,49])}%\n')
    print(f'Pregunta 3: Cual es la probabilidad de que se encuentre una persona con una edad menor de 49 años? {ansQuestions(49, 0, age, None)}%\n')
    print(f'Pregunta 4: Cual es la probabilidad de que se encuentre una persona con una edad entre 46 y 50 años? {ansQuestions(0, 2, age, [46,50])}%\n')
    print(f'Pregunta 5: Cual es la probabilidad de que las horas trabajadas sea mayor que 29,5 horas? {ansQuestions(29.5, 1, hoursWK, None)}%\n')
    print(f'Pregunta 6: Cual es la probabilidad de que las horas trabajadas sea menor que 26,5 horas? {ansQuestions(26.5, 1, hoursWK, None)}%\n')
    print("/------------------------------------------------------------------------------------------/\n")
    print('========== RACE SEX TABLE ==========')
    raceSexTable()
    print("/------------------------------------------------------------------------------------------/\n")
    print('========== AGE HOURS WK TABLE ==========')
    ageHoursWKTable()
    print("/------------------------------------------------------------------------------------------/\n")
    print('========== INCOME RANDOM SAMPLES TABLE AND QUESTIONS ==========')
    incomeRandomTable()
    print("/------------------------------------------------------------------------------------------/\n")
    print('========== AGE RANDOM SAMPLES TABLE AND QUESTIONS ==========')
    ageRandomTable()
    print("/------------------------------------------------------------------------------------------/\n")



def mainMenu():    
    ans = 0
    options = [
                    '- Sex', '- Age', '- Married', '- Income', '- Hours WK', '- Race', '- usCitizen', '- Health Insurance', '- languaje', '- Classic Data', '- Fase I', '- Fase II', '- Exit'
                ]
    while(ans < 13):
        print("\n================================================================")
        print("========================== MAIN MENU ===========================")
        print("================================================================")
        optChoice = cutie.select(options)
        ans = optChoice + 1
        
        if ans == 1:
            sexGraph()
        elif ans == 2:
            fillTable(age, "AGE", "0")
        elif ans == 3:
            marriedGraph()
        elif ans == 4:
            fillTable(income, "INCOME", "0")
        elif ans == 5:
            fillTable(hoursWK, "HOURS WORKING", "0")
        elif ans == 6:
            raceGraph()
        elif ans == 7:
            usCitizenGraph()
        elif ans == 8:
            healthInsurenceGraph()
        elif ans == 9:
            languageGraph()
        elif ans == 10:
            fillTable(testData, "OLD DATA", "0")
        elif ans == 11:
            showFaseI()
        elif ans == 12:
            showFaseII()
    print("=======================CLOSED=======================")


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

