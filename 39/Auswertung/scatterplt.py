import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

class ScatterPlotter:
    def __init__(self, title="", xlabel="", ylabel=""):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot(self, x, y, label=None, color='black', size=1, legend=True, grid=False):
        plt.scatter(x, y, label=label, c=color, s=size)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
        plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
        plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

        if legend:
            plt.legend()
        if grid:
            plt.grid(True)

    def show(self):
        plt.show()

    def save(self, filepath):
        plt.savefig(filepath)
        plt.close()
