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
        print(self.__data.max('frequency'))
    def getMin(self):
        return
    def getMedian(self):
        return