from pascaldata import PascalData
from matplotlib import pyplot as plt

# parsing the json file
data= PascalData("data/completo_black_3.json")
# creating the dataframe
df= data.times()
# converting string to float
df= df.astype(float)
# checking the available variables
print(df.columns)
# filtering the data
df= df[ (df["cores"] == 16)&(df["input"] == 5) ]
# ploting
df.plot(x="frequency", y="total_time")

asdasdasdasdasdasd
plt.show()