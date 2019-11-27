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
    print(data)
    #data.read()
    graphe=Graph()
    """graphe.read()"""
    setup.read(this_folder+os.sep+file)
    setup._colorframe='#4f81bd'
    root.configure(bg=setup._colorframe)
    MainWindow(root,setup,graphe)
    root.mainloop()
class setupFile():
    def __init__(self):
        self._colorbutton='#ffffff'
        self._colorflow='#ffffff'
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
                    if 'colorflow'in x:
                        self._colorflow=x[6]
                elif (filetype!='')and(filetype!='interface_setup'):
                    return('interface_setup')
                    break
class readJson():
    def __init__(self):
        self.input_file="d:\Profiles\igauthier\Documents\cours\completo_black_3.json"
    def read(self):
        result=PascalData(self.input_file)
if __name__=='__main__':
    main()