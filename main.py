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
    """#print (data.conf["data_descriptor"]["extras"]["sensors"]["values"][0])
    #print("aa")
    #print(data.res.keys())#["total_time"]"""
    datas=data.sens[(data.sens["sensors"].str.contains("ipmi"))]
    """#print("energy")
    #print(data.resu)
    #print(datas)
    datas2=data.res[(data.res["cores"] == 16)]
    print('test')
    print(datas2)"""
    datas3=data.resu
    """treat=Treatment(datas)
    treat2=Treatment(datas2)"""
    treat3=Treatment(datas3)
    datas3=treat3.init_type()
    """print(datas3)"""
    datas4=datas3[(datas3["frequency"]==1200000)]
    """print(datas3[(datas3["ipmi_energy"]==11683.448269)])"""
    treat4=Treatment(datas4)
    """maxi=treat2.getMax()
    maxim=treat3.getMax()"""
    datas4=treat4.init_type()
    """"""
    print('datas')
    print(datas4)
    maximu=treat4.getMax(datas4)
    print('size')
    print(datas4.shape)
    print(datas.shape)
    """print(maximu)
    mini=treat2.getMin()
    minim=treat3.getMin()"""
    minimu=treat4.getMin(datas4)
    print(datas4.loc[datas4['ipmi_energy']==minimu['ipmi_energy']])
    print(datas4.loc[datas4['ipmi_energy']==minimu['ipmi_energy']]['ipmi_power'])
    print(datas4.loc[datas4['ipmi_energy']==minimu['ipmi_energy']].index[0])
    print('dd')
    """#med=treat.getMedian()
    med2=treat2.getMedian()
    med3=treat3.getMedian()
    print('ipmi_power')
    print(datas4['ipmi_power'])"""
    med4=treat4.getMedian(datas4)
    """print(med2)
    #print('ee')
    moy2=treat2.getMean()
    moy3=treat3.getMean()"""
    moy4=treat4.getMean(datas4)
    """print(moy)
    PascalData.dataframe_group(moy,"sensors")
    #moy=10"""
    setupsoft=setup.read
    root.configure(bg=setup.colorframe)
    mainwindow=MainWindow(root,setup,treat4,datas4,data.conf)
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
        """#        self.__this_file=inspect.getfile(inspect.currentframe())
#        self.__this_folder=os.path.dirname(os.path.abspath(self.__this_file))
#        self.__this_filename=self.__this_folder+os.sep+self.__filename
#        with open(self.__this_filename,'r')as f:
#            for line_idx,line in enumerate(f):
#                temp=line.replace('>'," ")
#                y=tempo.lower()
#                x=y.split(' ')
#                self.__GoodFile=True"""

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