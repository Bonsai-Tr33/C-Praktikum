import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

class ScatterPlotter:
    def __init__(self, title="", xlabel="", ylabel=""):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot(self, x, y, label=None, color='black', size=1, legend=True, grid=False, xlim=False, ylim=False, xlimit=100, ylimit=1.2, xstep=10, ystep=10):
        plt.scatter(x, y, label=label, c=color, s=size, zorder=4)
        plt.axvline(x=0, color='grey', linestyle='--', zorder=1, alpha=0.5)
        plt.axhline(y=0, color='grey', linestyle='--', zorder=1, alpha=0.5)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
        plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
        plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

        # plt.xticks(np.arange(800000, 3000100, 200000))
        # plt.yticks(np.arange(8, 30, 1))
        # plt.ylim(-2, 7)

        if xlim:
            plt.xticks(np.arange(-(xlimit+5), xlimit+5, xstep))
            plt.xlim(-xlimit, xlimit)

        if ylim:
            plt.yticks(np.arange(-(ylimit+0.2), ylimit+0.2, ystep))
            plt.ylim(-ylimit, ylimit)

        if legend:
            plt.legend()
        if grid:
            plt.grid(True)

    def show(self):
        plt.show()

    def save(self, filepath, name):
        plt.savefig(filepath + name)
