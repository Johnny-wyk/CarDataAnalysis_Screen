# --coding:utf-8--

from myApp.models import *


def getAllCars():
    return carInfo.objects.all()