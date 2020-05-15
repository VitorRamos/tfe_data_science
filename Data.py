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
        # print(self.__data.dtypes)
        self.__data['frequency']=self.__data['frequency'].astype(int)
        self.__data['cores']=self.__data['cores'].astype(int)
        self.__data['input']=self.__data['input'].astype(int)
        self.__data['ipmi_power']=(self.__data['ipmi_power']).astype(float)
        self.__data['total_time']=(self.__data['total_time']).astype(float)
        self.__data['ipmi_energy']=(self.__data['ipmi_energy']).astype(float)
        # print(self.__data.dtypes)
        return self.__data
        
    def getMax(self,data):
        self.__maximum=data.max()
        # print('maximum')
        # print(self.__maximum)
        return self.__maximum

    def getMin(self,data):
        # print ('minimum')
        # print(self.__data)
        self.__minimum=data.min()
        """#print(np.nanmin(self.__data))
        print(self.__data.min()['ipmi_energy'])
        print('ll')
        print(self.__minimum)"""
        #print((self.__data['ipmi_energy']).min())
        return self.__minimum
        
    def getMedian(self,data):
        self.__median=data.median()
        return self.__median

    def getMean(self,data):
        """print(self.__data)"""
        self.__mean=data.mean()
        """print(mean)"""
        return self.__mean
    
    def getData(self):
        return self.__data
    
