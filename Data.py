import numpy as np
import statistics

class Treatment:
    """Class that manipulutes the datas.
        Attributes
            data - The whole set of data read
            maximum - The maximum of each type of data
            minimum - The minimum of each type of data
            median - The median of each type of data
            mean - The mean of each type of data
            medianEvolution - List of values of median related to the number of points considerated
            meanEvolution - List of values of mean related to the number of points considerated
        Methods
            getMax()
            getMin()
            getMedian()
            getMean()"""

    def __init__(self,data):
        self.__data=data
    
    def init_type(self):
        print(self.__data.dtypes)
        self.__data['frequency']=self.__data['frequency'].astype(int)
        self.__data['cores']=self.__data['cores'].astype(int)
        self.__data['input']=self.__data['input'].astype(int)
        self.__data['ipmi_power']=(self.__data['ipmi_power']).astype(float)
        self.__data['total_time']=(self.__data['total_time']).astype(float)
        self.__data['ipmi_energy']=(self.__data['ipmi_energy']).astype(float)
        print(self.__data.dtypes)
        return self.__data
        
    def getMax(self):
        self.__maximum=self.__data.max()
        return self.__maximum

    def getMin(self):
        """print ('minimum')
        print(self.__data)"""
        self.__minimum=self.__data.min()
        #print(np.nanmin(self.__data))
        return self.__minimum
        
    def getMedian(self):
        self.__median=self.__data.median()
        return self.__median

    def getMean(self):
        """print(self.__data)"""
        self.__mean=self.__data.mean()
        """print(mean)"""
    
    def getData(self):
        return self.__data
    
    def getMeanEvolution(self):
        return self.__meanEvolution
    
    def getMedianEvolution(self):
        return self.__medianEvolution
    
    def computeMeanEvolution(self):
        test=[]
        bus=[]
        for k in range(self.__data["ipmi_energy"].shape[0]):
            mean2=np.mean(self.__data["ipmi_power"].iloc[k])
            test.append(mean2)
            bus.append(statistics.mean(test))
            """print(bus)"""
        self.__meanEvolution=bus

    def computeMedianEvolution(self):
        """median3=[np.median(self.__data["ipmi_power"].iloc[k]) for k in range(self.__data["ipmi_energy"].shape[0])]
        median3=[self.__data["ipmi_power"].median(axis[k]) for k in range(self.__data["ipmi_energy"].shape[0])]
        median2=[np.median(self.__data["total_time"].iloc[k]) for k in range(self.__data["frequency"].shape[0])]
        print(median2)
        print(self.__data["ipmi_energy"].shape[0])"""
        print('median')
        test=[]
        bus=[]
        for k in range(self.__data["ipmi_energy"].shape[0]):
            median2=np.median(self.__data["ipmi_power"].iloc[k])
            test.append(median2)
            bus.append(statistics.median(test))
            """print(bus)
        print(bus)"""
        self.__medianEvolution=bus