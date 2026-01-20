import pandas as pd
import math

class Messreihe:
    def __init__(self, filepath, N1, N2, R=0.2, F=0.9, k=0.1):           # Loading CSV
        self.N1 = N1
        self.N2 = N2
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        second = self.data.columns[1]
        third = self.data.columns[2]

        self.data[second] = self.data[second].apply(lambda x: self.H(x, self.N1, R))
        self.data[third] = self.data[third].apply(lambda x: self.B(x, self.N2, F, k))
        self.data.columns = ['Time (s)','H(A/m)', 'B(T)']

    def H(self, U, N1, R):
        dm = 0.24
        return (N1*U)/(math.pi*dm*R)

    def B(self, U, N2, F, k):
        da = 0.26
        di = 0.22
        h = 0.03
        k = 0.1
        return U* k / (N2*(F*h*(da-di)/2))

    def dataArray(self):
        return self.data

    def show_head(self, n=5):               # Show first n Data frames
        return self.data.head(n)