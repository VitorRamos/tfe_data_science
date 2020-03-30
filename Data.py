import numpy as np
import statistics

class Treatment:

    """Class that manipulutes the datas.
        Attributes
            fig - The frame of the graph to draw
            ax1 - The choose of the datas to draw
        Methods
            getMax()
            getMin()
            getMedian()"""

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
        maximum=self.__data.max()
        return maximum

    def getMin(self):
        """print ('minimum')
        print(self.__data)"""
        minimum=self.__data.min()
        #print(np.nanmin(self.__data))
        return minimum

    def getMedian(self):
        """#print(self.__data)"""
        median3=[np.median(self.__data["ipmi_power"].iloc[k]) for k in range(self.__data["ipmi_energy"].shape[0])]
        """median3=[self.__data["ipmi_power"].median(axis[k]) for k in range(self.__data["ipmi_energy"].shape[0])]
        #median2=[np.median(self.__data["total_time"].iloc[k]) for k in range(self.__data["frequency"].shape[0])]
        print('aaaaaaaaaaaaaaaaaaaa')
        #print(median2)
        #print(self.__data["ipmi_energy"].shape[0])"""
        test=[]
        bus=[]
        for k in range(self.__data["ipmi_energy"].shape[0]):
            median2=np.median(self.__data["ipmi_power"].iloc[k])
            test.append(median2)
            bus.append(statistics.median(test))
            print(bus)
        #print(median2.shape)
        median=self.__data.median()
        print('median')
        print(median3)
        return bus

    def getMean(self):
        """print(self.__data)"""
        mean=self.__data.mean()
        print(mean)
        return mean