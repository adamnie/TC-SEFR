############
# Tabbed interface for TC-SEFR
############


from Tkinter import *
from PIL import Image, ImageTk
from lib.fractal import *
import numpy as np
import Tkconstants, tkFileDialog, tkHyperlinkManager
import time
import webbrowser
from threading import Timer
from main import *

BASE = RAISED
SELECTED = RIDGE
LANGUAGE = "EN"
VERBOSE = True

#FLAGS TO SHOW PROGRESS
checksum_flag = False
coefB_flag = False
coefC_flag = False
reconstr_flag = False
done_flag = False

#longer strings etc.
class Strings:
    if LANGUAGE == "PL":
        opis = """
Celem projektu jest implementacja algorytmu do samo-rekonstrukcji 
obrazow cyfrowych z wykorzystaniem kodowania fraktalnego. 
Samo-rekonstrukcja (ang. self-recovery lub self-embedding) pozwala
na weryfikacje integralnosci zdjecia oraz na odtworzenie jego 
oryginalnej tresci w oparciu o cyfrowy znak wodny. Opracowana 
w ramach projektu aplikacje nalezy wyposazyc w graficzny interfejs 
uzytkownika pozwalajacy na dostosowanie parametrow algorytmu oraz 
na zabezpieczanie i weryfikacje integralnosci obrazow cyfrowych.
        """
        decode_tab_name = "Zakoduj"
        code_tab_name = "Dekoduj"
        about_tab_name = "O programie"
        block_size_label = """
    Rozmiar bloku
    (domyslnie 3)
        """
        unable_to_open = "Nie mozna przetworzyc pliku. Sprobuj ponownie"
        data_label = "Dostosuj opcje:"
        save_data = "Zapisz dane"
        load_file = "Otworz plik"
        button_code = "Wykonaj kompresje i kodowanie"
        button_decode = "Wykonaj dekompresje i dekodowanie"
        in_progress = "Praca w toku..."
        about_title = "TC-SEFR \n Uwierzytelnianie obrazow cyfrowych \nz wykorzystaniem kodowania fraktalnego \n\n Adam Niedzialkowski, Antoni Grzanka \n Akademia Gorniczo-Hutnicza w Krakowie"
        visit_git = "Nasze repozytorium na GitHubie"

    else:
        opis = """\n\n
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
        data_label = "Configure options:"
        save_data = "Save data:"
        load_file = "Load file"
        button_code = "Perform compression and coding"
        button_decode = "Perform decompression and decoding"
        in_progress = "Working..."
        about_title = "TC-SEFR \n Authentication of digital image using fractal compression \n\n Adam Niedzialkowski, Antoni Grzanka \n AGH University of Science and Technology, Cracow"
        visit_git = "Visit out GitHub repository"

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
        Frame.__init__(self, master, height=500)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name
    
    def show(self):
        self.pack(side=TOP, fill=Y)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
    
    def add(self, tab, tab_img, tab_name):
        tab.pack_forget()                                   # hide the tab on init
        self.tabs[tab.tab_name] = tab                       # add it to the list of tabs
        b = Button(self, text=tab.tab_name, relief=BASE, command=(lambda name=tab.tab_name: self.switch_tab(name)))
        b.configure(image=tab_img)  
        b.configure(text=tab_name, compound=BOTTOM)
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

    def openfilename(self, which):
        #tkFileDialog
        try:
            filename = tkFileDialog.askopenfilename(**self.file_opt)
        except IOError:
            print Strings.unable_to_open  
        else:
            global image, imageToDecode, imageToDecode_thumb, image_thumb
            if which=="code":
                try:
                    image = img(filename)
                except IOError:
                    print Strings.unable_to_open 
                else:
                    image.setflags(write=True)
                    image.nazwa = filename
                    image.format = filename[-3:]
                    # resizing to fit the screen - does not support other than square!
                    image_thumb = image.resize((256,256))
                    image_thumb = preparePhotoImage(image_thumb)
                    # update image
                    img_code_label.configure(image=image_thumb)
                    img_code_label.image=image_thumb
                    CurrentData.refresh_img()
                    perform_button.configure(state=NORMAL)
            elif which=="decode":
                try:
                    imageToDecode = img(filename)
                except IOError:
                    print Strings.unable_to_open 
                else:
                    imageToDecode.setflags(write=True)
                    imageToDecode.nazwa = filename
                    imageToDecode.format = filename[-3:]
                    # resizing to fit the screen - does not support other than square!
                    imageToDecode_thumb = imageToDecode.resize((256,256))
                    imageToDecode_thumb = preparePhotoImage(imageToDecode_thumb)
                    # update image
                    img_decode_label.configure(image=imageToDecode_thumb)
                    img_decode_label.image=imageToDecode_thumb
                    CurrentData.refresh_imgDecode()
                    decode_button.configure(state=NORMAL)

class CurrentData:
    def refresh_opt(self):
        global sizeOfBlock
        title = "Current data: "
        blocksize="Blocksize: " + str(block_size_slider.get())
        sizeOfBlock = block_size_slide.get()
        sth = "Second: " + str(sth_slider.get())
        else_ = "Third: " + str(else_slider.get())
        what = "Fourth: " + str(what_slider.get())
        current_data=title + "\n" + blocksize + "    " + sth + "\n" + else_ + "    " + what
        current_data_label.configure(text=current_data)
    def refresh_img(self):
        title = "Image data: "
        img_name = "Filename: " + str(image.get_nazwa())
        img_format = "Format: " + str(image.format)
        img_size = "Image size: " + str(image.width()) + "x" + str(image.height())
        img_data = title + "\n" + img_name + "\n" + img_format + ", " + img_size
        img_data_label.configure(text=img_data)

    def refresh_imgDecode(self):
        title = "Image data: "
        img_name = "Filename: " + str(imageToDecode.get_nazwa())
        img_format = "Format: " + str(imageToDecode.format)
        img_size = "Image size: " + str(imageToDecode.width()) + "x" + str(imageToDecode.height())
        imgDecode_data = title + "\n" + img_name + "\n" + img_format + ", " + img_size
        imgDecode_data_label.configure(text=imgDecode_data)



def do_animation(currentframe, window, wrap, time_start, time_elapsed, which):
    def do_image(which):
        if which=="code":
            global code_animation
            wrap.delete('ani')
            wrap.create_image(80,100,image=code_animation[currentframe], tag='ani')
        elif which=="decode":
            global decode_animation
            wrap.delete('ani')
            wrap.create_image(80,100,image=decode_animation[currentframe], tag='ani')            
    try:
        do_image(which)
    except IndexError:
        currentframe = 0
        do_image(which)
    wrap.update_idletasks() #Force redraw
    time_now = time.clock()
    time_elapsed.set(secondformat(time_now-time_start))
    currentframe = currentframe + 1
    # Call myself again to keep the animation running in a loop
    window.after(100, do_animation, currentframe, window, wrap, time_start, time_elapsed, which)

def secondformat(nr):

    nr *= 1000
    nr = int(nr)
    ms = nr % 10
    nr -= ms
    nr /= 10
    seconds = nr%60
    minutes = (nr - seconds)/60
    
    if (seconds<10):
        secondsS = "0" + str(seconds)
    else:
        secondsS = str(seconds)
    
    if (minutes == 0):
        minutesS = "0"
    else:
        minutesS = str(minutes)
    
    msS = str(ms)
    return minutesS + ":" + secondsS + "." + msS  
    
# function that instantly updates label's text
def updateLabel(what, w):
    what.configure(text=w)

# marks label as done
def markAsDone(what, w):
    global done
    what.configure(image=done)


code_animation = []
decode_animation = []
sizeOfBlock = 3

class Handlers:
    def perform(self):
        global code_animation, done, image
       
        def finished(window, label):
            label.configure(text="Finished!")
            t = Timer(2.0, window.destroy)
            t.start()

        print "Called perform handler (which does almost nothing)!"
        window = Toplevel(root)
        for i in range(0,77):
            if i in range(0,10):
                num = "0" + str(i)
            else:
                num = str(i)
            filename = "animation/code" + num + ".gif"
            code_animation.append(PhotoImage(file=filename))
        window.overrideredirect(1)
        working_label = Label(window, text=Strings.in_progress)
        working_label.pack(expand=YES, fill=BOTH)
        wrap = Canvas(window, width=160, height=200)
        wrap.pack(expand=YES, fill=BOTH)
        time_start = time.clock()
        time_now = time.clock()
        time_elapsed = StringVar()
        time_elapsed.set(secondformat(time_now-time_start))
        time_label = Label(window, textvariable=time_elapsed)
        time_label.pack(expand=YES, fill=X)
        button_stop = Button(window, text="STOP", command=lambda:Handlers.destroywindow(window))
        button_stop.pack(expand=YES, fill=BOTH)
        window.after(10, do_animation, 0, window, wrap, time_start, time_elapsed, "code")
        window.geometry("+" + str(SCREEN_WIDTH/2 - 160/2) + "+" + str(SCREEN_HEIGHT/2 - 200/2) )

        # t4 = Timer(6.0, finished, (window, working_label))
        # t4.start()
        
        fractalObject = perform_compression(image,sizeOfBlock,True)

        window.mainloop()

    def destroywindow(self, window):
        print "Stopped!"
        window.destroy()

    def decode(self):
        global decode_animation, checksum_flag, coefC_flag, coefB_flag, done_flag, reconstr_flag, imageToDecode

        # finish and close small window
        def finished(window, label):
            label.configure(text="Finished!")
            t = Timer(2.0, window.destroy)
            t.start()

        print "Called decode handler (which does almost nothing)!"
        window = Toplevel(root)
        for i in range(0,77):
            if i in range(0,10):
                num = "0" + str(i)
            else:
                num = str(i)
            filename = "animation/decode" + num + ".gif"
            decode_animation.append(PhotoImage(file=filename))
        window.overrideredirect(1)
        working_label = Label(window, text=Strings.in_progress)
        working_label.grid(row=0, column=0, columnspan=2)

        wrap = Canvas(window, width=160, height=200)
        wrap.grid(row=1, column=0, columnspan=2)
        time_start = time.clock()
        time_now = time.clock()
        time_elapsed = StringVar()
        time_elapsed.set(secondformat(time_now-time_start))

        none = PhotoImage(file="images/none.gif")
       
        checksum_done = Label(window,image=none)
        checksum_done.grid(row=3, column=0, sticky=E)
        checksum = Label(window, text="Checksum... ")
        checksum.grid(row=3,column=1, sticky=W)

        coefB_done = Label(window, image=none)
        coefB_done.grid(row=4,column=0, sticky=E)
        coefB = Label(window, text="Calculating B... ")
        coefB.grid(row=4,column=1, sticky=W)

        coefC_done = Label(window, image=none)
        coefC_done.grid(row=5,column=0, sticky=E)
        coefC = Label(window, text="Calculating C... ")
        coefC.grid(row=5,column=1, sticky=W)

        reconstr_done = Label(window, image=none)
        reconstr_done.grid(row=6, column=0, sticky=E)
        reconstr = Label(window, text="Reconstructing...")
        reconstr.grid(row=6,column=1, sticky=W)

        # przyklady "zapalania" poszczegolnych "lampek" 
        #
        # wykonano coefB: 
        # markAsDone(coefB_done, "done")
        #
        #


        #
        # t = Timer(5.0, markAsDone, (checksum_done, "done"))
        # t.start()

        # t2 = Timer(3.0, markAsDone, (coefB_done, "done"))
        # t2.start()

        # t3 = Timer(4.0, markAsDone, (coefC_done, "done"))
        # t3.start()



        # zakonczono?
        # wywolaj finished(window, working_label)
        t4 = Timer(6.0, finished, (window, working_label))
        t4.start()


        time_label = Label(window, textvariable=time_elapsed)
        time_label.grid(row=7, column=0, columnspan=2)
        button_stop = Button(window, text="STOP", command=lambda:Handlers.destroywindow(window))
        button_stop.grid(row=8, column=0, columnspan=2)
        window.after(10, do_animation, 0, window, wrap, time_start, time_elapsed, "decode")
        window.geometry("+" + str(SCREEN_WIDTH/2 - 160/2) + "+" + str(SCREEN_HEIGHT/2 - 200/2) )
        window.mainloop()




def preparePhotoImage(img):
    """ Input is any kind of ndarray, output is PhotoImage"""
    imageArr = img.view(np.ndarray)
    imageInst= Image.fromarray(imageArr, "L")
    return ImageTk.PhotoImage(imageInst)


def toConsole(x): print x


# FANCY GRAPHICS


# MAIN PART
root = Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
Dialogue = Dialogue(root)
CurrentData = CurrentData()
Handlers = Handlers()
root.title("TC-SEFR - Antoni Grzanka, Adam Niedzialkowski")
root.geometry("700x600" + "+" + str(SCREEN_WIDTH/2 - 700/2) + "+" + str(SCREEN_HEIGHT/2 - 600/2) )
root.resizable(0,0)

done = PhotoImage(file="images/ok.gif")
image = img("pictures/noimg.pgm")
imageToDecode = img("pictures/noimg.pgm")


bar = TabBar(root)

# ABOUT TAB
about_tab = Tab(root, Strings.about_tab_name)

space2_label = Label(about_tab, text="                   ")
space2_label.grid(row=0,column=0,columnspan=2)
 
kt_logo = PhotoImage(file="images/ktlogo.gif")
kt_logo_label = Label(about_tab, image=kt_logo)
kt_logo_label.grid(row=1,column=0, pady=10, sticky=N)

iet_logo = PhotoImage(file="images/ietlogo.gif")
iet_logo_label = Label(about_tab, image=iet_logo)
iet_logo_label.grid(row=2, column=0, pady=10, sticky=N)

agh_logo = PhotoImage(file="images/aghlogo.gif")
agh_logo_label = Label(about_tab, image=agh_logo)
agh_logo_label.grid(row=3, column=0, pady=10, sticky=N)

space3_label = Label(about_tab, text= "   ")
space3_label.grid(row=0, column=1, rowspan=4)

title_label = Label(about_tab, text=Strings.about_title, font="Verdana 10 bold")
title_label.grid(row=1, column=2, padx=30)

opis_label = Label(about_tab, text=Strings.opis)
opis_label.grid(row=2, column=2, rowspan=2, padx=30, sticky=N)

git_logo = PhotoImage(file="images/gitlogo.gif")
git_button = Button(about_tab, image=git_logo, compound=LEFT, text=Strings.visit_git, command=lambda: webbrowser.open("https://github.com/adamnie/TC-SEFR"))
git_button.grid(row=4, column=0, columnspan=3, sticky=S, pady=20)

# CODE AND SET WATERMARK
code_tab = Tab(root, Strings.code_tab_name)

#image is an Image instance that we are really working with
#image_thumb is the PhotoImage instance that is shown on screen (resized)
image = img("pictures/noimg.pgm")
image.setflags(write=True) 
image_thumb = image.resize((256,256))
image_thumb = preparePhotoImage(image_thumb)

img_code_label = Label(code_tab, image=image_thumb)
img_code_label.image=image_thumb
img_code_label.grid(row=2,column=2, rowspan=6, padx=50)

space_label = Label(code_tab, text="                   ")
space_label.grid(row=0,column=0,columnspan=3)

open_button = Button(code_tab, text=Strings.load_file, command=lambda:Dialogue.openfilename("code"))
open_button.grid(row=1,column=2)    

data_label = Label(code_tab, text=Strings.data_label)
data_label.grid(row=2, column=0, columnspan=2)

block_size_label = Label(code_tab, text=Strings.block_size_label)
block_size_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
block_size_label.grid(row=2,column=0)
block_size_slider.grid(row=2,column=1)

sth_label = Label(code_tab, text=Strings.block_size_label)
sth_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
sth_label.grid(row=3,column=0)
sth_slider.grid(row=3,column=1)

else_label = Label(code_tab, text=Strings.block_size_label)
else_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
else_label.grid(row=4,column=0)
else_slider.grid(row=4,column=1)

what_label = Label(code_tab, text=Strings.block_size_label)
what_slider = Scale(code_tab, from_=2, to=6, orient=HORIZONTAL)
what_label.grid(row=5,column=0)
what_slider.grid(row=5,column=1)

refresh_data_button = Button(code_tab, text=Strings.save_data, command=CurrentData.refresh_opt)
refresh_data_button.grid(row=6,column=0, columnspan=2)

current_data="blah"
img_data = "blah"
current_data_label = Label(code_tab, text=current_data)
img_data_label = Label(code_tab, text=img_data)
CurrentData.refresh_opt()
CurrentData.refresh_img()
current_data_label.grid(row=8,column=0,columnspan=2, pady=10)
img_data_label.grid(row=8, column=2, pady=10)

perform_button = Button(code_tab, text=Strings.button_code, command=Handlers.perform, state=DISABLED)
perform_button.grid(row=9, column=0, columnspan=3)

# DECODE
decode_tab = Tab(root, Strings.decode_tab_name)
imageToDecode = img("pictures/noimg.pgm")
imageToDecode.setflags(write=True) 
imageToDecode_thumb = image.resize((256,256))
imageToDecode_thumb = preparePhotoImage(imageToDecode_thumb)
img_decode_label = Label(decode_tab, image=imageToDecode_thumb)
img_decode_label.image=imageToDecode_thumb
img_decode_label.grid(row=2,column=2, rowspan=6, padx=50)


spaceDecode_label = Label(decode_tab, text="                   ")
spaceDecode_label.grid(row=0,column=0,columnspan=3)

openToDecode_button = Button(decode_tab, text=Strings.load_file, command=lambda:Dialogue.openfilename("decode"))
openToDecode_button.grid(row=1,column=2, pady=10)    

imgDecode_data = "blah"
imgDecode_data_label = Label(decode_tab, text=imgDecode_data)
CurrentData.refresh_imgDecode()
imgDecode_data_label.grid(row=8, column=2, pady=10)

decode_button = Button(decode_tab, text=Strings.button_decode, command=Handlers.decode, state=DISABLED)
decode_button.grid(row=9, column=0, columnspan=3)

# IMPORTING IMAGES
code_tab_button = PhotoImage(file="images/button_code.gif")
decode_tab_button = PhotoImage(file="images/button_decode.gif")
about_tab_button = PhotoImage(file="images/button_about.gif")


# ADDING TABS TO BAR
bar.add(code_tab, code_tab_button, Strings.code_tab_name)
bar.add(decode_tab, decode_tab_button, Strings.decode_tab_name)
bar.add(about_tab, about_tab_button, Strings.about_tab_name)

bar.show()

root.mainloop()