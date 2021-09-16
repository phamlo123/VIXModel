import pandas as pd
import numpy as np

strikeDelta = 5


class ProcessingAndFeaturing:

    def __init__ (self, forecastHorizon, numStrikesSelected, timeStamp: list, listOfOptions: list):
        self.forecastHorizon = forecastHorizon
        self.numStrikeSelected = numStrikesSelected
        self.timeStamp = timeStamp
        self.listOfOptions = listOfOptions
        self.listOfOptionsPrice = {}

    def strikeSelection (self, ATMStrike: list) -> list:
        selectedStrike = []
        for i in range (len (self.timeStamp)):
            selectedStrikeCall = []
            selectedStrikePut = []
            for i in range (self.numStrikeSelected):
                selectedStrikeCall.append (ATMStrike[i] + strikeDelta)
                selectedStrikePut.append (ATMStrike[i] - strikeDelta)

            selectedStrike.append (selectedStrikePut)
            selectedStrike.append (selectedStrikeCall)

        selectedStrike.append (ATMStrike)
        return selectedStrike

    def featureEngineering (self, ATMStrike: list):
        selectedStrike = self.strikeSelection (ATMStrike)
        for i in range(len (self.timeStamp)):


