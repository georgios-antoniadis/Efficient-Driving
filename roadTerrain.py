import numpy as np

class road():
    def __init__(self):
        #Assuming driving inside a city
        #All values are in km/h
        self.speedlimitLower = 10 * (10**3) / (60*60*60) #Normally there is no such limit but we pick a value to make it realistic
        self.speedlimitUpper = 48 * (10**3) / (60*60*60)
        self.incline = False
        self.theta = 0 