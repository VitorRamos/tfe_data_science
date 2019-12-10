import inspect,os,matplotlib
from pascaldata import PascalData
from GUI import Graph
from GUI import MainWindow
from tkinter import tix
root=tix.Tk()

def main():
    file='interface_setup.txt'
    this_file=inspect.getfile(inspect.currentframe())
    this_folder=os.path.dirname(os.path.abspath(this_file))
    setup=setupFile()
    data=readJson()
    data.read()
    datas=data.res[(data.res["input"]==5)]
    graphe=Graph(datas)
    """graphe.read()"""
    setup.read(this_folder+os.sep+file)
    setup._colorframe='#4f81bd'
    root.configure(bg=setup._colorframe)
    MainWindow(root,setup,graphe,datas)
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
        self._colorbutton='#ffffff'
        self._colorframe='#ffffff'
    
    def read(self,filename):
        GoodFile=False
        filetype=''
        with open(filename,'r')as f:
            for line_idx,line in enumerate(f):
                temp=line.replace('>'," ")
                tempo=temp.replace('<',' ')
                y=tempo.lower()
                x=y.split(' ')
                if ('filetype'in x)or (GoodFile==True):
                    if 'filetype'in x:
                        filetype=x[6]
                        if filetype=='interface_setup':
                            GoodFile=True
                    if 'colorframe'in x:
                        self._colorframe=x[6]
                    if 'colorbutton'in x:
                        self._colorbutton=x[6]
                elif (filetype!='')and(filetype!='interface_setup'):
                    return('interface_setup')
                    break

class readJson():
    """ Class that read the file in JSON format contaning the results
        Attributes
            input_file - The name of the file of results in input
        Methods
            read()"""
    
    def __init__(self):
        """ Create a empty object and initialize attribute."""
        self.input_file="d:\Profiles\igauthier\Documents\cours\completo_black_3.json"
    
    def read(self):
        result=PascalData(self.input_file)
        datas=result.times()
        self.res=datas.astype(float)

if __name__=='__main__':
    main()