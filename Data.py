import numpy as np

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
        #self.__data["frequency"].astype(int)
        #self.__data["cores"].astype(int)
        #self.__data["input"].astype(int)
        self.__data=self.__data.astype(int)
        print(self.__data.dtypes)
        return self.__data
        
    def getMax(self):
        maximum=self.__data.max()
        return maximum

    def getMin(self):
        minimum=self.__data.min()
        return minimum

    def getMedian(self):
        print(self.__data)
        median=self.__data.median()
        print(median)
        return median

    def getMean(self):
        print(self.__data)
        mean=self.__data.mean()
        print(mean)
        return mean