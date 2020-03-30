# -*- coding: utf-8 -*- 
import pandas as pd
import inspect,os,matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
from pylab import plot,axis,savefig,show,title
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from tkinter import filedialog, messagebox
from tkinter import *
#from matplotlib.lines import Line2D

class Graph:
    """ Class that read the draw the different graphes
        Attributes
            fig - The frame of the graph to draw
            ax1 - The choose of the datas to draw
        Methods
            sliders_on_changed()
            simpleGraphe()
            twoGraphes()"""

    def __init__(self,data,master,choice):
        """ Create a empty object and initialize attributes."""
        self.__master=master
        self.__data=data.getData()
        self.__fig = Figure(figsize=(12,7), dpi=50)
        self.__canvas=FigureCanvasTkAgg(self.__fig,master=self.__master)
        """print("data ini")
        #self.__data= self.__data.astype(int)
        #print(self.__data["frequency"].dtype)
        print(self.__data["frequency"])
        #self.__data_disp=self.__data["ipmi_power"]"""
        self.__data_disp= self.__data#[self.__data["frequency"]==1200000]
        """print("data test")
        print(data.dtypes)"""
        self.__canvas.get_tk_widget().place(x=650,y=10)
        self.__max=data.getMax()
        self.__min=data.getMin()
        self.__median=data.getMedianEvolution()
        """print(self.__data_disp.dtypes)
        print(self.__data_disp["ipmi_power"].shape)
        print(self.__data_disp["ipmi_energy"].shape)
        print('median')
        print(self.__median)
        self.__fig.add_subplot(111).plot(self.__data_disp["ipmi_energy"],self.__median, 'r--')""" 
        if choice == 'L':
            self.__fig.add_subplot(111).plot(self.__data_disp["ipmi_energy"],self.__median, 'r--') 
            self.__axis, = self.__fig.add_subplot(111).plot(self.__data_disp["ipmi_energy"],self.__data_disp["ipmi_power"])
        if choice == 'B':    
            self.__axis= self.__fig.add_subplot(111)
            N=1428
            ind = np.arange(N)
            width = 0.35
            self.__axis.bar(ind,self.__data_disp["ipmi_energy"],width)
        """print('median')
        print(self.__median)"""
        if choice == 'P':
            print('ah')
            self.__axis= self.__fig.add_subplot(111)
            self.__axis.scatter(self.__data_disp["ipmi_energy"],self.__median,c='red', marker = "o")
            self.__axis.scatter(self.__data_disp["ipmi_energy"],self.__data_disp["ipmi_power"], marker = "x")
            #plt.show()
        print('ouf')
        self.__graph=self.simpleGraphe(data)
        
    #def read(self):
        #wine_reviews=pd.read_csv("d:\Profiles\igauthier\Downloads/beatsdataset.csv")
        #plot([1,2,3,4],[1,4,9,16])
        #axis([1,4,0,16])
        #title('my curve')
        #savefig('acurvesaved.png')
        #show()

    def sliders_on_changed(self,val):
        """Display a sliding bar controlling a variable.
        :param val: The variable to modify"""
        self.__freq=self.sfreq.val
        #print("frequence")
        #print(self.__freq)
        self.__core=self.scores.val
        print("core")
        print(self.__core)
        self.__input=self.sinput.val
        #print("input")
        #print(self.__input)
        self.__data_disp=self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
        #&(self.__data["cores"]==self.__core)]
        print("data")
        print(self.__data_disp)
        self.__axis.set_xdata(self.__data_disp["ipmi_energy"])
        self.__axis.set_ydata(self.__data_disp["ipmi_power"])
        print(self.__data_disp.dtypes)
        print(self.__data_disp["ipmi_power"].shape)
        print(self.__data_disp["ipmi_energy"].shape)
        self.__a=self.__fig.canvas.draw_idle()

    def simpleGraphe(self,data):
        """The graph to draw.
        :param master: The window where to draw the graph.
        :param data: The data to draw."""
        #canvas.columnconfigure(1, pad=3)
        #plt.add_subplot(111).plot(data["frequency"],data["cores"])
        #self.__canvas.draw()
        self.__fig.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        self.__axfreq=self.__fig.add_axes([0.2, 0.11, 0.6, 0.03], facecolor=self.__axcolor)
        self.__axcore=self.__fig.add_axes([0.2, 0.07, 0.6, 0.03], facecolor=self.__axcolor)
        self.__axinput=self.__fig.add_axes([0.2, 0.03, 0.6, 0.03], facecolor=self.__axcolor)
        self.sfreq=Slider(self.__axfreq,'Frequency',self.__min["frequency"],self.__max["frequency"],valinit=self.__min["frequency"],
            valstep=100000)
        self.scores=Slider(self.__axcore,'Cores',self.__min["cores"],self.__max["cores"], valinit=self.__min["cores"],valstep=1)
        self.sinput=Slider(self.__axinput,'Input',self.__min["input"],self.__max["input"], valinit=self.__min["input"],valstep=1)
        self.sfreq.on_changed(self.sliders_on_changed)
        self.scores.on_changed(self.sliders_on_changed)
        self.sinput.on_changed(self.sliders_on_changed)
        #print(self.sfreq.val)
        #self.__data_disp=data[(data["frequency"]==self.sfreq)]
        print("power")
        print(self.__data_disp["ipmi_power"])
        #self.__canvas.show()
        #self.__fig.pause(0.01)

    @property
    def twoGraphes(self):
        """Creating to graph to compare them."""
        self.__graphe1=plt.subplots(131)
        self.__ax=self.__fig.add_axes([0.1,0.1,0.8,0.8])
        self.__graphe2=plt.subplots(132)
        self.__names=['groupa','groupb','groupc']
        self.__values=['1','10','100']
        plot(names,values)
        self.__canvas=FigureCanvasTkAgg(self.__fig)
        """canvas.show()"""
        self.__canvas.get_tk_widget().place(x=300,y=40)

    def reset(self):
        print(self.__data)
        self.sfreq.reset()
        self.scores.reset()
        self.sinput.reset()
        self.__graphini=self.simpleGraphe(self.__data)

    def updateType(self,choice):
        self.__fig.clf()
        if choice == 'L':
            self.__fig.add_subplot(111).plot(self.__data_disp["ipmi_energy"],self.__median, 'r--') 
            self.__axis, = self.__fig.add_subplot(111).plot(self.__data_disp["ipmi_energy"],self.__data_disp["ipmi_power"])
        if choice == 'B':    
            self.__axis= self.__fig.add_subplot(111)
            N=1428
            ind = np.arange(N)
            width = 0.35
            self.__axis.bar(ind,self.__data_disp["ipmi_energy"],width)
        if choice == 'P':
            self.__axis= self.__fig.add_subplot(111)
            self.__axis.scatter(self.__data_disp["ipmi_energy"],self.__median,c='red', marker = "o")
            self.__axis.scatter(self.__data_disp["ipmi_energy"],self.__data_disp["ipmi_power"], marker = "x")
        print(self.__data)
        self.__graph=self.simpleGraphe(self.__data)

class MainWindow:
    """ Class that read the setup file
        Attributes
            setup - The 
            graphe - The frame containing the graph
        Methods
            initGUI()
            graphes()
            MenuBar()
            quit()
            ok()"""

    def __init__(self,master,setup,datas,data,conf):
        """ Create a empty object and initialize attributes and GUI with graphe and initGUI methods.
        :param data: Data to draw"""
        self.__setup=setup
        #print("start")
        #print(datas["ipmi_power"])
        """self.graphe.createWidgets()"""
        self.__master=master
        """self.frame=Frame(self.master)"""
        self.__confi=conf
        self.__max=datas.getMax()
        self.__min=datas.getMin()
        self.__median=datas.getMedian()
        self.__mean=datas.getMean()
        self.__label_2=None
        self.__label_3=None
        self.__label_4=None
        self.__label_5=None
        self.__label_6=None
        self.__label_7=None
        self.__label_8=None
        self.__label_9=None
        self.__label_10=None
        self.__choice='C'
        self.initGUI(datas)
        
    def close_window(self):
        global running
        running = False
    
    def initGUI(self,data):
        """Creation of the different object.
        :param data: Data to display"""
        self.__master.protocol("WM_DELETE_WINDOW", self.close_window())
        self.__RWidth=self.__master.winfo_screenwidth()
        self.__RHeight=self.__master.winfo_screenheight()
        self.__master.geometry(str(self.__RWidth)+"x"+str(self.__RHeight))
        self.__master.title('Test')
        self.__master.configure(bg=self.__setup.colorframe)
        self.MenuBar()
        choice=self.typeGraph()
        self.__graphe=Graph(data,self.__master,'L')
        self.graphes(data.getData())
        self.__closebutton = Button(self.__master, text='X', command=self.quit)
        """self.canvas1=tix.Canvas(self.master, width=390, height=600)
        self.canvas1.place(x=230,y=40)
        self.canvas1.config(bg=self.setup._colorframe,bd=0)"""

    def graphes(self,data):
        """Creation of the graph.
        :param data: Data to draw"""
        var=[]
        """self.__graph=self.__graphe.simpleGraphe(self.__master,data)"""
        self.__label_1=Label(self.__master,text='VARIABLES LIST',justify=LEFT).pack(expand=0,anchor='w')
        for i in range (len(self.__confi["data_descriptor"])):
            vartemp=BooleanVar()
            var.append(vartemp)
            self.__checkbutton_1=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["keys"][i],
                variable=lambda index=i:var[index],onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',justify='left',
                command=lambda index=i:self.update_text(var,index)).pack(expand=0,anchor='w')

    def update_text(self,var,i):
        print(i)
        print(self.__label_2)
        print(var[i].get())
        if i==0:
            if self.__label_2==None:
                self.__label_2=Label(self.__master,text='Cores',justify=LEFT)
                self.__label_2.place(x=650,y=450)
                self.__label_3=Label(self.__master,text='Minimum : '+str(self.__min["cores"]),justify=LEFT)
                self.__label_3.place(x=650,y=470)
                self.__label_4=Label(self.__master,text='Maximum : '+str(self.__max["cores"]),justify=LEFT)
                self.__label_4.place(x=650,y=490)
            else:
                self.__label_2.destroy()
                self.__label_3.place_forget()
                self.__label_4.place_forget()
                self.__label_2=None
        if i==1:
            if self.__label_5==None:
                self.__label_5=Label(self.__master,text='Frequency',justify=LEFT)
                self.__label_5.place(x=650,y=510)
                self.__label_6=Label(self.__master,text='Minimum : '+str(self.__min["frequency"]),justify=LEFT)
                self.__label_6.place(x=650,y=530)
                self.__label_7=Label(self.__master,text='Maximum : '+str(self.__max["frequency"]),justify=LEFT)
                self.__label_7.place(x=650,y=550)
            else:
                self.__label_5.destroy()
                self.__label_6.place_forget()
                self.__label_7.place_forget()
                self.__label_5=None
        if i==2:        
            if self.__label_8==None:
                self.__label_8=Label(self.__master,text='Input',justify=LEFT)
                self.__label_8.place(x=650,y=570)
                self.__label_9=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_9.place(x=650,y=590)
                self.__label_10=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_10.place(x=650,y=610)
            else:
                self.__label_8.destroy()
                self.__label_9.place_forget()
                self.__label_10.place_forget()
                self.__label_8=None
        #self.__label_11=Label(self.__master,text='Repetitions',justify=LEFT).pack(expand=0,anchor='w')
        #self.__label_12=Label(self.__master,text='Minimum : '+str(self.__min["repetitions"]),justify=LEFT).pack(expand=0,anchor='w')
        #self.__label_13=Label(self.__master,text='Maximum : '+str(self.__max["repetitions"]),justify=LEFT).pack(expand=0,anchor='w')
                                    
    def MenuBar(self):
        """This method is called by the initialisation of the interface to 
        create a bar with the different menu."""
        self.__menu = Menu(self.__master)
        self.__master.config(menu=self.__menu)
        #create the different menu.
        self.__filemenu = Menu(self.__menu)
        self.__howtomenu=Menu(self.__menu)
        self.__var9=IntVar()
        self.__var10=IntVar()
        self.__var11=IntVar()
        self.__var12=IntVar()
        self.__var13=IntVar()
        self.__menu.add_cascade(label="Menu", menu=self.__filemenu)
        self.__menu.add_cascade(label="Information", menu=self.__howtomenu)
        #create the different option for the menus.
        self.__howtomenu.add_command(label="Help", command=self.how_to)
        self.__howtomenu.add_command(label='Loading files', command=self.load_file)
        self.__howtomenu.add_command(label="aa")      
        self.__filemenu.add_command(label="Reset", command=self.reset)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.quit)
    
    def reset(self):
        self.__graphe.reset()

    def quit(self):
        """This method is called by the pushing on the 'Exit' menu to close the
        software."""
        if messagebox.askyesno('Verify', 'Do you really to quit?'):
            sys.exit()
    
    def ok(self):
        """This method is called by the 'quit' method to close the main window."""
        self.__master.withdraw()

    def how_to(self):
        """This method is called by the pushing on the 'Help' menu to display in
        a pop_up window the help to use the software."""
        #create the new window with the 'Manual Book' title.
        self.__newWindow = Toplevel(self.__master)
        self.__master=self.__newWindow
        self.__master.title('Manual Book')
        self.__master.geometry("700x430+10+10")
        #display the text
        self.__label_20=Label(self.__master,text="Help: text to write").place(x=215,y=15,width=300,height=25)

    def load_file(self):
        """This method is called by the pushing on the 'Loading file' menu to 
        upload the right result file for the session."""
        #read the session file thanks to the object session.
        self.__name= filedialog.askopenfilename()
        print(self.__name)

    def uncheckall(self,checktest,cbs):
        print(checktest)
        i=1
        for cb in cbs:
            print('i')
            print(i)
            if i == checktest:
                print('top')
                cb.select()
            else:
                print('ouf')
                cb.deselect()
            i=i+1
        print('test')
        print(checktest)
        if checktest == 2 :
            self.__choice = 'B'
        else :
            if checktest == 3 :
                self.__choice = 'P'
            else:
                self.__choice = 'L'
        print(self.__choice)
        self.updateGraph()

    def updateGraph(self):
        self.__graphe.updateType(self.__choice)
        
    def typeGraph(self):
        var1=BooleanVar()
        var2=BooleanVar()
        var3=BooleanVar()
        self.__checkbutton_10=Checkbutton(self.__master,text='Lignes',variable=var1,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(1,cbs),justify='left')
        self.__checkbutton_11=Checkbutton(self.__master,text='Bars',variable=var2,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(2,cbs),justify='left')
        self.__checkbutton_12=Checkbutton(self.__master,text='Points',variable=var3,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(3,cbs),justify='left')
        cbs = [self.__checkbutton_10, self.__checkbutton_11, self.__checkbutton_12]
        self.__checkbutton_12.place(x=800,y=500)
        self.__checkbutton_11.place(x=800,y=475)
        self.__checkbutton_10.place(x=800,y=450)#ack(expand=0,anchor='e')