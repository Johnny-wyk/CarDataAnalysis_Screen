# --coding:utf-8--
import json
import time
import re
from .getPublicData import *

def getCircleData():
    cars = list(getAllCars())
    oilData = []
    electricData = []
    for i in cars:
        if i.energyType == '汽油':
            oilData.append([i.carName,i.saleVolume,i.energyType])
        elif i.energyType == '纯电动':
            electricData.append([i.carName,i.saleVolume,i.energyType])
    oilData = oilData[:10]
    electricData = electricData[:10]
    return oilData,electricData