from pascaldata import PascalData
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# parsing the json file
data= PascalData("data/completo_black_3.json")
# creating the dataframe
df= data.times()
# converting string to float
df= df.astype(float)
# checking the available variables
print(df.columns)
# filtering the data
df= df[ (df["input"] == 5) ]

# ploting
fig = plt.figure()
ax = fig.gca(projection='3d')
X= df["frequency"]
Y= df["cores"]
Z= df["total_time"]
ax.plot_trisurf(X, Y, Z, antialiased=True, color="r")

plt.show()