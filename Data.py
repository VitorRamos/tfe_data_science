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
    def getMax(self):
        maximum=self.__data.max()
        print(maximum["frequency"])
        return maximum
    def getMin(self):
        minimum=self.__data.min()
        print(minimum["frequency"])
        return minimum
    def getMedian(self):
        print ("bb")
        print(self.__data)
        median=self.__data.median()
        print(median)
        return median