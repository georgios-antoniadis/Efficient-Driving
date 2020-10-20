import numpy as np

#Specs link https://www.edmunds.com/ford/fiesta/2019/features-specs/
mass = 1169.361 
mu = 0.7
g = 9.8
fuelTank = 46.93911
fuelEnergy = 32.6*(10**6)*fuelTank
print(fuelEnergy)

uNeeded = 50000/(60*60) #Set a journey of about an avg speed of 50km/h
acceleration = uNeeded/(11.5/2) #In m/s^2. Time taken from a 0-100 of about 11.5

Facc = mass*acceleration
u = 0 #Track of position
x = 0 #Track of place

time = 0 #Track of time
positions = []

"""
while u <= uNeeded:
    x += (1/2)*acceleration*(time**2)
    u += acceleration*time
    print(u)
    positions.append(x)
    time += 1
"""
friction  = mu*mass*g

i = 0
print(i)
while fuelEnergy > 0:
    fuelEnergy -= mu*mass*g
    i += 1
    positions.append(i)

print(max(positions))

#This is a message for my future self
