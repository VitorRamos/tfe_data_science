import inspect,os,matplotlib
import xml.etree.ElementTree as ET
from pascaldata import PascalData
from Data import Treatment
from GUI import MainWindow, Graph
from tkinter import tix
root=tix.Tk()

def main():
    setup=setupFile()
    data=readJson()
    datatemp=data.read
    #print (data.conf["data_descriptor"]["extras"]["sensors"]["values"][0])
    #print("aa")
    #print(data.res.keys())#["total_time"]
    datas=data.sens[(data.sens["sensors"].str.contains("ipmi"))]
    #print("energy")
    #print(data.resu)
    #print(datas)
    datas2=data.res[(data.res["cores"] == 16)]
    datas3=data.resu
    treat=Treatment(datas)
    treat2=Treatment(datas2)
    treat3=Treatment(datas3)
    maxi=treat2.getMax()
    maxim=treat3.getMax()
    datas3=treat3.init_type()
    #print(maxi)
    mini=treat2.getMin()
    minim=treat3.getMin()
    #print(minim)
    med=treat.getMedian()
    #print('dd')
    med2=treat3.getMedian()
    #print(med2)
    #print('ee')
    moy=treat3.getMean()
    #print(moy)
    #PascalData.dataframe_group(moy,"sensors")
    #moy=10
    setupsoft=setup.read
    root.configure(bg=setup.colorframe)
    mainwindow=MainWindow(root,setup,datas3,datas,data.conf,maxim, minim,med2,moy)
    root.mainloop()

class setupFile():
    """ Class that read the setup file
        Attributes
            colorbutton - The color for the button
            colorframe - The color for the window
        Methods
            read()"""
    
    def __init__(self):
        """ Create a empty object and initialize attributes."""
        self.colorbutton='#ffffff'
        self.colorframe='#ffffff'
        self.__GoodFile=False
        self.__filetype=''
        self.__filename='interface_setup.txt'
        
    @property
    def read(self):
        """Read the file with the name given.
        :param filename: Filename of the file to read"""
#        self.__this_file=inspect.getfile(inspect.currentframe())
#        self.__this_folder=os.path.dirname(os.path.abspath(self.__this_file))
#        self.__this_filename=self.__this_folder+os.sep+self.__filename
#        with open(self.__this_filename,'r')as f:
#            for line_idx,line in enumerate(f):
#                temp=line.replace('>'," ")
#                y=tempo.lower()
#                x=y.split(' ')
#                self.__GoodFile=True
        tree=ET.parse(self.__filename)
        root=tree.getroot()
        self.__filetype=root[0][0].text
        self.colorframe=root[1][0].text
        self.colorbutton=root[1][1].text

class readJson():
    """ Class that read the file in JSON format contaning the results
        Attributes
            input_file - The name of the file of results in input
        Methods
            read()"""
    
    def __init__(self):
        """ Create a empty object and initialize attribute."""
        self.__input_file="d:\Profiles\igauthier\Documents\cours\completo_black_3.json"
    
    @property
    def read(self):
        """Read the file containing the data to display"""
        self.__result=PascalData(self.__input_file)
        self.conf=self.__result.config
        test=self.__result.dataframe_generic()
        self.sens=self.__result.dataframe_group("sensors")
        self.resu=self.__result.energy("mean")
        self.__datas=self.__result.times()
        self.res=self.__datas.astype(float)

if __name__=='__main__':
    main()