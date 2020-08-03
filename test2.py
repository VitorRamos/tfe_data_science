<<<<<<< Updated upstream
testb
=======
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xlist = [1, 2, 3, 4, 5]
ylist = [1, 5, 3, 4, 2]
zlist = [6, -3, 6, -1, 2]
zmin = np.min(zlist)
print(zmin)
mask = np.array(zlist) == zmin
print(np.array(zlist))
print(mask)
color = np.where(mask, 'red', 'blue')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xlist, ylist, zlist, color=color)
#plt.ticklabel_format(useOffset=False)   
plt.show()
>>>>>>> Stashed changes
