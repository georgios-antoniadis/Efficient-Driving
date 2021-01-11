import csv
import matplotlib.pyplot as plt

rpm = []
fuel = []

fuelDens = 0.7489 #Grams per litres
usefulConv = 200 #Converting to litres per 100km

#Expected line
expectFuel = []
expectedX = []
for i in range(1000,6000,500):
  expectedX.append(i)
  expectFuel.append(i*(999/4)*0.001*(1/15)*1.29*(2.2*60)*fuelDens*0.001)

for i in range(1,24):
  path = 'dataLog'+str(i)+'.csv'
  dataFile = open(path, newline = '')
  reader = csv.reader(dataFile)
  for row in reader:
    if ' Distance' in row:
      pass
    else:
      if len(row) > 3:
        if float(row[1]) == 500:
          rpm.append(float(row[2]))
          fuel.append(float(row[3])*fuelDens*10**(-5)*usefulConv)

#plt.plot(rpm,fuel,'ro')
#plt.plot(expectedX,expectFuel,'b--')
plt.scatter(rpm,fuel,c=fuel,cmap='RdYlGn', s=50)
plt.xlabel('rpm')
plt.ylabel('fuel in litres/100km')
plt.show()  
