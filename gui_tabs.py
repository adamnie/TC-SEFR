############
# Tabbed interface for TC-SEFR
############


from Tkinter import *
from PIL import Image, ImageTk
from fractal import *
import numpy as np
import Tkconstants, tkFileDialog

BASE = RAISED
SELECTED = FLAT
LANGUAGE = "EN"
VERBOSE = True

#longer strings etc.
class Strings:
    if LANGUAGE == "PL":
        opis = """
Jestesmy super, fajny projekt
blabla
blablablabla
Lorem ipsum
        """
        decode_tab_name = "Zakoduj"
        code_tab_name = "Dekoduj"
        about_tab_name = "O programie"
        block_size_label = """
    Rozmiar bloku
    (domyslnie 3)
        """
        unable_to_open = "Nie mozna przetworzyc pliku. Sprobuj ponownie"

    else:
        opis = """
The aim of the project is to implement an algorithm for
self-reconstruction of digital images using
fractal coding. Self-reconstruction (called self-recovery
or self-embedding) allows you to verify the integrity of the
images and to reconstruct the original content based on the
digital watermark. Application developed in the project must
be equipped with a graphical user interface that allows you
to adjust the algorithm parameters and to protect and verify
the integrity of digital image
        """
        decode_tab_name = "Decode"
        code_tab_name = "Encode"
        about_tab_name = "About"
        block_size_label = """
    Block size
    (default 3)
        """
        unable_to_open = "Unable to open/parse file. Try again"


fractal = fractal()
Strings = Strings()

# a base tab class
class Tab(Frame):
    def __init__(self, master, name):
        Frame.__init__(self, master, width=700, height=400)
        self.pack_propagate(0)
        self.tab_name = name

# bar displaying tabs
class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master, height=100)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name
    
    def show(self):
        self.pack(side=TOP, expand=YES, fill=Y)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
    
    def add(self, tab):
        tab.pack_forget()                                   # hide the tab on init
        
        self.tabs[tab.tab_name] = tab                       # add it to the list of tabs
        b = Button(self, text=tab.tab_name, relief=BASE,    # basic button stuff
            command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        b.pack(side=LEFT)                                               # pack the buttont to the left mose of self
        self.buttons[tab.tab_name] = b                                          # add it to the list of buttons
    
    def delete(self, tabname):
        
        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])
        
        else: del self.tabs[tabname]
        
        self.buttons[tabname].pack_forget()
        del self.buttons[tabname] 
        
    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=BASE)
            self.tabs[self.current_tab].pack_forget()           # hide the current tab
        self.tabs[name].pack(side=TOP, expand=YES, fill=Y)   # tu grzebalem                        # add the new tab to the display
        self.current_tab = name                                 # set the current tab to itself
        
        self.buttons[name].config(relief=SELECTED)                  # set it to the selected style

class Dialogue:
    def __init__(self, root):
        # default options for opening file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

    def openfilename(self):

        #tkFileDialog
        try:
            filename = tkFileDialog.askopenfilename(**self.file_opt)
        except IOError:
            print Strings.unable_to_open  
        # open file with my own code
        if filename:
            global image
            try:
                image = fractal.open_img_PGM(filename)
            except IOError:
                print Strings.unable_to_open  
            image.setflags(write=True) 
            img_code_prepared = preparePhotoImage(image)
            # update image
            img_code_label.configure(image=img_code_prepared)
            img_code_label.image=img_code_prepared
            CurrentData.refresh()

class CurrentData:
    def refresh(self):
        title = "Current data: "
        img_size = "Image size " + str(image.width()) + "x" + str(image.height())
        blocksize="Blocksize " + str(block_size_slider.get())
        sth = "Second " + str(sth_slider.get())
        else_ = "Third " + str(else_slider.get())
        what = "Fourth " + str(what_slider.get())
        current_data=title + "\n" + img_size + "\n" + blocksize + "\n" + sth + "\n" + else_ + "\n" + what
        current_data_label.configure(text=current_data)



def preparePhotoImage(img):
    """ Input is any kind of ndarray, output is PhotoImage"""
    imageArr = img.view(np.ndarray)
    imageInst= Image.fromarray(imageArr, "L")
    return ImageTk.PhotoImage(imageInst)


def toConsole(x): print x


# MAIN PART
root = Tk()
Dialogue = Dialogue(root)
CurrentData = CurrentData()
root.title("TC-SEFR - Antoni Grzanka, Adam Niedzialkowski")
root.geometry("700x500")
root.resizable(0,0)

bar = TabBar(root)

# ABOUT TAB
about_tab = Tab(root, Strings.about_tab_name)               # notice how this one's master is the root instead of the bar
Label(about_tab, text=Strings.opis, bg="white", fg="red").pack(side=TOP, expand=YES, fill=BOTH)

# CODE AND SET WATERMARK
code_tab = Tab(root, Strings.code_tab_name)

image = fractal.open_img_PGM("noimg.pgm")
image.setflags(write=True) 
img_code_prepared = preparePhotoImage(image)
img_code_label = Label(code_tab, image=img_code_prepared)
img_code_label.grid(row=0,column=2, rowspan=6, padx=50)

open_button = Button(code_tab, text="Load file", command=Dialogue.openfilename)
open_button.grid(row=0,column=0, columnspan=2)    

block_size_label = Label(code_tab, text=Strings.block_size_label)
block_size_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
block_size_label.grid(row=1,column=0)
block_size_slider.grid(row=1,column=1)

sth_label = Label(code_tab, text=Strings.block_size_label)
sth_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
sth_label.grid(row=2,column=0)
sth_slider.grid(row=2,column=1)

else_label = Label(code_tab, text=Strings.block_size_label)
else_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
else_label.grid(row=3,column=0)
else_slider.grid(row=3,column=1)

what_label = Label(code_tab, text=Strings.block_size_label)
what_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
what_label.grid(row=4,column=0)
what_slider.grid(row=4,column=1)

refresh_data_button = Button(code_tab, text="Save data", command=CurrentData.refresh)
refresh_data_button.grid(row=5,column=0, columnspan=2)

current_data="blah"
current_data_label = Label(code_tab, text=current_data)
CurrentData.refresh()
current_data_label.grid(row=6,column=0,columnspan=3, pady=10)

# DECODE
decode_tab = Tab(root, Strings.decode_tab_name)        
img_decode_tab = preparePhotoImage(image)
Label(decode_tab, bg='white', image=img_decode_tab).pack(side=LEFT, expand=YES, fill=BOTH)

# ADDING TABS TO BAR
bar.add(code_tab)
bar.add(decode_tab)
bar.add(about_tab)

bar.show()


root.mainloop()


