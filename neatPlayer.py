import numpy as np
from roadTerrain import road
import pygame

carPng = pygame.image.load('carImage.png')
w, h = w, h = 1000,600 #Dimension of my window

gears = [3.417,1.958,1.276,0.943,0.757,0.634]

"""
The current draft is an oversimplified version
Velocity and acceleration are very poorly calculated
The same can be said for the fuel energy

"""

road = road()

carImage = pygame.image.load('carImage.png')

"""
Car picked for this scenario is the 2020 ford fiesta
Specs can be found here: https://www.automobile-catalog.com/car/2020/2562920/ford_fiesta_1_0_ecoboost_125.html
"""

class player():
    def __init__(self,goal,road):
        self.mass = 1391 + 75 #Assuming a single 75 kg passenger
        self.throttle = 0
        self.breaking = 0
        self.zeroToHundred = 11.2 #In seconds
        self.tyreRollingCoefficient = 0.01 # tyre rolling resistance coefficient
        self.position = 0
        self.alive = True
        self.goal = goal
        self.velFail = 0
        self.image = carImage
        
        #Drag
        self.dragCoefficient = 0.321
        self.carArea = 0.690 #In m^2

        #Road
        self.road = road

        #Speed
        self.acceleration = 0
        self.accel = False
        self.velocityConversion = (10**3) / (60*60*60)
        self.maxVelocity = self.road.speedlimitUpper
        self.velocity = self.road.speedlimitLower

        #Revolutions
        self.maxRpm = 6400 / (60*60) #In revs per 1/60th of a second. Actually the redline on the rpm meter
        self.idleRpm = 700 / (60*60) #In revs per 1/60th of a second
        self.rpm = self.idleRpm

        #Engine
        self.hp = 123 #Horsepower
        self.engineDisplacement = 999 #In cm^3
        self.numberOfCylinders = 4

        #Gearing
        self.gearRatio = gears[0]
        self.gearRatioIndex = 1
        self.axleRatio = 3.941

        #Tyres
        self.tyreRadius = (((16*25.4)/2) + (195*(55/100))) * (10**(-3)) #in m
        self.tyreMass = 8 #In kg as an average

        #Fuel
        self.gasolineDensity = 800#g/liter
        self.fuelCapacity = 42*self.gasolineDensity #in g.
        #self.fuelEnergy = 32.6*(10**6)*self.fuelCapacity #In Joules
        self.airDensity = 1.29 #grams per liter
        self.compressionRatio = 17
        self.fuelUsed = 0

        #Road
        self.road = road

        #Font
        self.statFont = pygame.font.SysFont('comicsans',35)

        #Driver
        self.gasPressure = 0

    #Shifting gears
    def shifting(self,index):
        if index == 'up' and self.gearRatioIndex < len(gears) and self.velocity > 0:
            self.gearRatioIndex += 1
        elif index == 'down' and self.gearRatioIndex > 2:
            self.gearRatioIndex -= 1
        elif index == 'down' and self.gearRatioIndex == 1:
            self.gearRatioIndex -= 1 #Neutral

        if self.gearRatioIndex > 0:
            self.gearRatio = gears[self.gearRatioIndex - 1]
        #Lifting the foot of the throttle
        self.gasPressure = 0

    #Pressing the throttle
    def accelerating(self,pressure,gasPressurePoints):
        
        #Drag
        fDrag = 1/2*self.dragCoefficient*self.airDensity*(self.velocity**2)*self.carArea
        aDrag = fDrag/(self.mass)

        aRolling = (self.tyreRollingCoefficient * 9.8 ) / (60*60)

        self.gasPressure = pressure
        if self.gasPressure > 0 and self.gearRatioIndex > 0: #Pressing the gas pedal while in gear
            self.accel = True
            maxAcceleration = (100*self.velocityConversion) / (self.zeroToHundred*60) #Acceleration in m/s^2
            self.throttle = self.gasPressure
            if self.road.incline:
                #self.acceleration = maxAcceleration * self.throttle - (9.8*np.sin(self.road.theta*(np.pi/180) / (60*60))) No drag
                self.acceleration = maxAcceleration * self.throttle - aDrag - aRolling
            else:
                #self.acceleration = maxAcceleration * self.throttle
                self.acceleration = maxAcceleration * self.throttle - aDrag - aRolling

        elif self.gasPressure <= 0 or self.gearRatioIndex == 0: #Not pressing throttle or in neutral
            self.accel = False
            if self.road.incline:
                self.acceleration = -(aRolling + aDrag*2 + (9.8*np.sin(self.road.theta*(np.pi/180) / (60*60)))) 
                #self.acceleration = -self.tyreFrictionCoefficient * 9.8 / (60*60) - (9.8*np.sin(self.road.theta*(np.pi/180) / (60*60)))
            else:
                self.acceleration = -(aDrag*2+aRolling) 
                #self.acceleration = -self.tyreFrictionCoefficient * 9.8 / (60*60) #Since F = ma and F = -mgμ where μ the tyre friction coefficient

    def maxVel(self):
        ''' 
        Calculating the maximum velocity possible on a givern gear
        Got help from here:
        https://www.quora.com/Why-is-the-maximum-speed-limit-in-the-first-gear-in-a-car-40kmph
        Basically Max velocity = max car rpm * (1/gear ratio) * tyre circumference
        '''
        if self.gearRatioIndex > 0:
            self.maxGearVelocity = self.maxRpm * (1/self.gearRatio) * (1/self.axleRatio) * (self.tyreRadius * 2 * np.pi) 

        #Changing the stall rpm of the engine based on the gear
        #Note that although we are changing the variable idleRpm we are basically changing stall rpm
        if self.gearRatioIndex > 1 and self.gearRatioIndex <= 3:
            self.idleRpm = 1000 / (60*60) #Basically anything other than 1st gear will stall at 1000 rpm
        if self.gearRatioIndex > 3 and self.gearRatioIndex <= 6:
            self.idleRpm = 1200 / (60*60) #Basically anything other than 1st gear will stall at 1000 rpm

    #Moving the car
    def move(self):
        #Changing things up. Using the very simple throttle code we are gonna calculate the
        #car's RPM and hence the energy it uses.

        if self.accel:
            #Car is not allowed to exceed its limits
            if self.maxGearVelocity > self.maxVelocity:
                self.maxGearVelocity = self.maxVelocity

            if self.velocity + self.acceleration > 0:
                if self.velocity < self.maxGearVelocity:
                    self.velocity += self.acceleration #Iterating velocity
                else:
                    self.velocity = self.maxGearVelocity
        else:
            self.velocity += self.acceleration

        #Finding the rpm of the car
        wheelRotation = self.velocity / self.tyreRadius
        
        if self.gearRatioIndex > 0: #Car in gear
            self.rpm = wheelRotation * self.gearRatio * self.axleRatio * (1/(2*np.pi))
        else: #Car in neutral
            self.rpm = 700 / (60*60)

        if self.rpm > self.maxRpm:
            self.rpm = self.maxRpm

        self.position += self.velocity
        self.checkGoal() #Checking if we have crossed the line
    
    #Calculating the energy it loses
    def fuelUse(self):
        #Finding fuel used solely from how much is going into the engine every given dt
        if self.accel:
            airFuelRatio = 1/15.7
            airUsed = self.rpm * (self.engineDisplacement / self.numberOfCylinders) * 0.001 #Turns cm^3 to litres
            massOfAirUsed = airUsed * self.airDensity
            self.fuelUsed = massOfAirUsed * airFuelRatio / 1000
        else:
            self.fuelUsed = 0
        
        self.fuelCapacity -= self.fuelUsed

    #Drawing the car graphics on the screen
    def draw(self,win,index):
        #Shorter version
        if self.alive:
            win.blit(self.image,((self.position),(index+1)*25))
            #Speed
            text = self.statFont.render(str(round(self.velocity*(1/self.velocityConversion))),1,(0,255,0))
            win.blit(text,((self.position)+20,(index+1)*25+40))
            #Rpm
            rpmText = self.statFont.render(str(round(self.rpm*(60*60))),1,(255,0,0))
            win.blit(rpmText,((self.position)+20,(index+1)*25+60))
            #Gears
            rpmText = self.statFont.render(str(self.gearRatioIndex),1,(255,0,0))
            win.blit(rpmText,((self.position)+80,(index+1)*25+50))

    #Check if it crosses the line
    def checkGoal(self):
        self.alive = True
        if self.position > self.goal:
            self.alive = False

    def getAlive(self):
        return self.alive
