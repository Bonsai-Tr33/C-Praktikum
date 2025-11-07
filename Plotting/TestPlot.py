from Plotting import PlotHelper

xvalue = [1,3,5,7,9,11]
yvalue = [0,2,4,6,8,12]
xerr = [0,0,0,0,0,0,]
yerr = [0.2, 0.2, 0.5, 0.5, 0.2, 0.2]

Draw = PlotHelper('/Users/Moritz/Library/CloudStorage/OneDrive-Personal/Dokumente/Uni/Qutie FS5/C-Praktikum/Plotting/Images')
Draw.standardPlot(xvalue, yvalue)
