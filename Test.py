import csv
import matplotlib.pyplot as plt


values = []

with open("Datosproyecto2024.csv", newline="") as dataBase:
    spamreader = csv.reader(dataBase, delimiter=" ", quotechar=" ")
    i = 0
    for row in spamreader:
        if i > 0:
            data = row[0].split(",")
            values.append(data[5])
        i = 1

plt.hist(values)
plt.show()