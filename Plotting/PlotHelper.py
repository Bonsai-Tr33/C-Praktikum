import matplotlib.pyplot as plt
class PlotHelper:
    def __init__(self, plotPath):
        self.plotPath = plotPath
    
    def __str__(self):
        pass

    def standardPlot(self, xArray, yArray, xerr, yerr, curveLabel, Labelx='x-Axis', Labely='y-Axis', Title='Plot', grid=False):
        plt.errorbar(xArray, yArray, xerr=xerr, yerr=yerr, fmt='x', label=curveLabel, capsize=4)
        plt.xlabel(Labelx)
        plt.ylabel(Labely)
        plt.title(Title)
        if grid:
            plt.grid(True)
        else:
            plt.grid(False)
        plt.legend()
        plt.show()
        plt.savefig(self.plotPath + f'/{Title}')
        
    
