# measuring the speed of light

# dependencies
import numpy as np
import os
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path

def c(x,t):
    return  2* (x-0.2315) / t

Orte = [3.91, 4.02, 4.14, 7.92, 8.03, 8.15, 11.712, 11.822, 11.942]
Zeit = [24*10**(-9), 24*10**(-9), 28*10**(-9), 50*10**(-9), 52*10**(-9), 58*10**(-9), 78*10**(-9), 80*10**(-9), 86*10**(-9)]

Bip = []
for i in range(len(Orte)):
    Bip.append(c(Orte[i], Zeit[i]))

print(sum(Bip)/len(Bip))
