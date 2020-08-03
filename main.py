import inspect,os,matplotlib
import xml.etree.ElementTree as ET
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from pascaldata import PascalData
from Data import Treatment
from GUI2 import MainWindow, Graph
from tkinter import tix
root=tix.Tk()

def main():
    setup=setupFile()
    name="d:\Profiles\igauthier\Documents\cours\TFE\completo_xhpl_2.json"
    datajs=readJson(name)
    datatemp=datajs.read
    datas=datajs.sens[(datajs.sens["sensors"].str.contains("ipmi"))]
    """datas2=data.res[(data.res["cores"] == 16)]"""
    datas3=datajs.resu
    """treat=Treatment(datas)
    treat2=Treatment(datas2)"""
    treat3=Treatment(datas3)
    datas3=treat3.init_type()
    datas4=datas3[(datas3["frequency"]==1200000)]
    treat4=Treatment(datas4)
    """maxi=treat2.getMax()
    maxim=treat3.getMax()"""
    datas4=treat4.init_type()
    """maximu=treat4.getMax(datas4)
    mini=treat2.getMin()
    minim=treat3.getMin()"""
    """minimu=treat4.getMin(datas4)
    med=treat.getMedian()
    med2=treat2.getMedian()
    med3=treat3.getMedian()"""
    """med4=treat4.getMedian(datas4)
    moy2=treat2.getMean()
    moy3=treat3.getMean()
    moy4=treat4.getMean(datas4)"""
    setupsoft=setup.read
    root.configure(bg=setup.colorframe)
    saved=SaveData()
    mainwindow=MainWindow(root,setup,treat3,datas3,datajs.conf,saved,name)
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
    
    def __init__(self,nom):
        """ Create a empty object and initialize attribute."""
        self.__input_file=nom
        print('aa',self.__input_file)
    
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

class SaveData():
    def __init__(self):
        print("saving operation")

    def saveJson(self,namefile,data,axeX1,axeX2,axeY1,axeY2):
        name=os.path.splitext(namefile)[0]
        name=name+"_axeX1_"+axeX1+"_axeY1_"+axeY1+"_axeX2_"+axeX2+"_axeY2_"+axeY2+".json"
        test=PascalData()
        test.save_data(name)
        data.to_json(name)

    def savePDF(self,namefile,data,axeX1,axeX2,axeY1,axeY2):
        name=os.path.splitext(namefile)[0]
        name=name+"_axeX1_"+axeX1+"_axeY1_"+axeY1+"_axeX2_"+axeX2+"_axeY2_"+axeY2+".pdf"
        pdftest=PdfPages(name)
        pdftest.savefig(data,bbox_inches='tight')
        pdftest.close()

if __name__=='__main__':
    main()