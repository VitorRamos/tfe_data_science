from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

# Adjust the plot region to leave some space for the slider
plt.subplots_adjust(bottom=0.25)

# plot something
plt.plot([1,2,3])

# create the slider
x0, y0, witdth, heigth= 0.15, 0.05, 0.70, 0.05
axInput= plt.axes([x0, y0, witdth, heigth], facecolor='lightgoldenrodyellow')
sin1 = Slider(ax=axInput, label="test", valmin=0, valmax=100, valinit=50)

plt.show()