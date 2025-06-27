import tkinter as tk
import pandas as pd
from typing_extensions import IntVar
from PIL import ImageTk, Image
import os
import csv
import uuid
from TextState import TextState

def getImageList(ImagePath='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/'):
    dir = [file for file in os.listdir(ImagePath) if file.endswith('.tif')]
    return [os.path.join(ImagePath,file) for file in dir]

def getImage(image_path,max_size=(1000,2000)):
    img = Image.open(image_path)
    img.thumbnail(max_size)
    return ImageTk.PhotoImage(img)

def create_gui():

    window = tk.Tk()
    window.geometry('1920x1080')
    window.title("Data Verifyer")  # Set the window title


    # For Image, place it in ttk.Frame first
    # NOTE: be careful, by defauult the parent size is set by their children. We can change this by frame.pack_propogate(False)
    # img_frame = tk.Frame(window, width=800,height=1000,borderwidth=10, relief=tk.RIDGE)
    # img_frame.pack_propagate(False)
    # img_frame.grid(row=0,column=0,columnspan=2,rowspan=2)
    #
    # text_frame = tk.Frame(window,width=800,height=800,borderwidth=10,relief=tk.RIDGE)
    # text_frame.pack_propagate(False)
    # text_frame.grid(row=0,column=3)
    #
    # label = tk.Label(img_frame,text="Image Placeholder")
    # label.pack()
    #
    # label2 = tk.Label(text_frame,text="Lorus Ipsum this is tons of text!\n And multiple lines too!")
    # label2.pack()




    # # Create a Button widget
    # next_button = tk.Button(window, text="Next", command=window.destroy)
    # prev_button = tk.Button(window, text="Prev", command=window.destroy)
    # submit_button = tk.Button(window, text="Submit", command=window.destroy)
    # prev_button.grid(row=4,column=0)
    # submit_button.grid(row=4,column=1)
    # next_button.grid(row=4,column=2)

    window.mainloop()

def importData(file_name):
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path = os.path.join(back_dir,'outputs','txt_extract.csv')
    df = pd.read_csv(path)

    source_name = os.path.splitext(os.path.basename(file_name))[0]
    s = df[df['source']==source_name]

    return s['name_data'], s['food_data'], s['found_edibility']


class ImageState:
    def __init__(self,image_path,filter_ls=None,debug_mode=False,img_max_size=(1440,1080)):
        self.index=0
        if filter_ls:
            self.image_ls = [os.path.join(image_path,file) for file in os.listdir(image_path) if file.endswith('.tif') and file.split('.')[0] in filter_ls]
        else:
            self.image_ls = [os.path.join(image_path,file) for file in os.listdir(image_path) if file.endswith('.tif')]
        self.image_ls.sort()
        self.image_path=self.image_ls[self.index]
        self.img_max_size=img_max_size
        self.length = len(self.image_ls)
        self.file_name = os.path.splitext(os.path.basename(self.image_ls[self.index]))[0]
        self.debug_mode=debug_mode

        # self.currImg = self.getImage()

    def setLabel(self,label):
        self.label = label
        return

    def updateName(self):
        file = self.image_ls[self.index]
        self.image_path = file
        self.file_name = os.path.splitext(os.path.basename(file))[0]

        if self.debug_mode:
            print('Name Updated! ',self.file_name)
        return

    def next(self):
        # checks that we are not at last index
        if self.index < self.length - 1:
            self.index += 1
            self.updateName()
        else:
            # If we hit next at last index, position to first element of list
            self.index = 0
            self.updateName()
        if self.debug_mode:
            print('Next Index:',self.index)

    def prev(self):
        # If we are at first index and hit prev, we go to last item in the list
        if self.index == 0:
            self.index = -1
            self.updateName()
        else:
            self.index -= 1
            self.updateName()

        if self.debug_mode:
            print('Previous Index:',self.index)

    def getImage(self):
        img = Image.open(self.image_path)
        img.thumbnail(self.img_max_size)
        return ImageTk.PhotoImage(img)



def gui2(file_filter=None):
    # Need something that manages program state!
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    Is = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/',filter_ls=file_filter,debug_mode=True)
    Ts = TextState(txt_path=os.path.join(back_dir,'outputs','txt_files'),filter_ls=file_filter,debug_mode=True)

    window = tk.Tk()
    session_id = uuid.uuid4()
    window.geometry('1920x1080')
    window.title("Data Verifyer")  # Set the window title

    # Two Major Frames
    dframe = tk.Frame(window,height=1080,width=810,borderwidth=10,relief=tk.RIDGE) # display frame, 900x1600
    cframe = tk.Frame(window,height=860,width=860,borderwidth=10,relief=tk.RIDGE)
    iframe = tk.Frame(window,height=540,width=860,borderwidth=10,relief=tk.RIDGE) # input frame, 180,1600
    # iframe = tk.Frame(window,height=1080,width=860,borderwidth=10,relief=tk.RIDGE) # input frame, 180,1600

    dframe.pack_propagate(False)
    dframe.pack(side='left',padx=50) #top

    cframe.pack_propagate(False)
    cframe.pack()
    iframe.pack_propagate(False)
    iframe.pack(side='bottom')

    # Display Frame - Showing Images
        # Image - change image on click
    # ms = getImageList()
    # img = getImage(ms[0],max_size=(1440,1080))
    img = Is.getImage()
    img_label = tk.Label(dframe,image=img)
    img_label.pack()
    # img_label.grid(row=0,column=0)


    # CSV Frame - Json or CSV
    txt = Ts.getText()
    txt_label = tk.Label(cframe,text=txt)
    txt_label.pack()



    # Click events
        # Image - change on click, depending on prev/next
        # Submit - append name, and text boxes to .csv

    # Entry Boxes
    l_species = tk.Label(iframe,text='Species')
    l_edible = tk.Label(iframe,text='Edible Parts')
    species_box = tk.Entry(iframe)
    edible_box = tk.Entry(iframe)

    l_species.grid(row=1,column=0)
    l_edible.grid(row=2,column=0)
    species_box.grid(row=1,column=1)
    edible_box.grid(row=2,column=1)

    # Check Box
    multiple_species = tk.IntVar()
    several_pages = tk.IntVar()
    unused = tk.IntVar()
    cbox_multiple_species = tk.Checkbutton(iframe,text="Multiple species present",variable=multiple_species,onvalue=1,offvalue=0)
    cbox_several_pages = tk.Checkbutton(iframe,text="Spans Several Pages",variable=several_pages,onvalue=1,offvalue=0)
    cbox_unused = tk.Checkbutton(iframe,text="Unused Page",variable=unused,onvalue=1,offvalue=0)

    cbox_multiple_species.grid(row=0,column=0)
    cbox_several_pages.grid(row=0,column=1)
    cbox_unused.grid(row=0,column=2)

    # Buttons

    def update():
        # Update Image Display
        img=Is.getImage()
        img_label.config(image=img)
        img_label.image=img

        # Update Text Display
        txt = Ts.getText()
        txt_label.config(text=txt)
        txt_label.text=txt

        # Clear Text Boxes
        sb = species_box.get()
        eb = edible_box.get()
        if sb:
            species_box.delete(0,tk.END)
        if eb:
            edible_box.delete(0,tk.END)

        # Clear Check Boxes
        multiple_species.set(0)
        several_pages.set(0)
        unused.set(0)
        return

    def next():
        Is.next()
        Ts.next()
        update()
        return

    def prev():
        Is.prev()
        Ts.prev()
        update()
        return

    def submit_click():
        # Checking source name
        source = Is.file_name
        if '.' in source:
            source = source.split('.')[0]

        # Creating data string
        # SCHEMA: source | name_data | food_data | multiple_species | several_pages | unused
        data = [source, species_box.get(), edible_box.get(),multiple_species.get(),several_pages.get(),unused.get()]

        # Setting up csv path, write/append mode, and writer
        back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        output_csv = os.path.join(back_dir,'outputs','gui',f'{session_id}.csv')
        if not os.path.exists(output_csv):
            csv_mode = 'w'
        else:
            csv_mode = 'a'

        with open(output_csv,csv_mode) as file:
            writer = csv.writer(file)
            writer.writerow(data)

        return


    next_button = tk.Button(iframe, text="Next", command=next)
    prev_button = tk.Button(iframe, text="Prev", command=prev)
    submit_button = tk.Button(iframe, text="Submit", command=submit_click)

    prev_button.grid(row=3,column=0)
    submit_button.grid(row=3,column=1)
    next_button.grid(row=3,column=2)



    window.mainloop()

def test_ImageState():
    Is = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/',debug_mode=True)
    print('Init Index ',Is.index)
    print('Init Filename ',Is.file_name)

    Is.next()

def test_TextState():
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    Ts = TextState(txt_path=os.path.join(back_dir,'outputs','txt_files'),debug_mode=True)

    test_text = Ts.getText()
    print(test_text)

    Ts.next()
    test_text = Ts.getText()
    print(test_text)
    return


if __name__ == "__main__":
    # Creating filter list
    import pandas as pd
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    df = pd.read_csv(os.path.join(back_dir,'outputs','txt_extract.csv'))
    # print(df.shape)
    df = df[df['found_edibilty']==False]
    # print(df.shape)
    filter_ls = df['source'].map(lambda x: x.split('.')[0]).to_list()




    # create_gui()
    gui2(file_filter=filter_ls)
    # test_ImageState()
    # test_TextState()
