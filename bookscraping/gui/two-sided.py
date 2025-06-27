import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image
import os
import csv
import uuid
from TextState import TextState
from ImageState import ImageState




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
    dframe_l = tk.Frame(window,height=1080,width=810,borderwidth=10,relief=tk.RIDGE) # display frame, 900x1600
    dframe_r = tk.Frame(window,height=1080,width=810,borderwidth=10,relief=tk.RIDGE) # display frame, 900x1600
    iframe = tk.Frame(window,height=540,width=300,borderwidth=10,relief=tk.RIDGE) # input frame, 180,1600
    # iframe = tk.Frame(window,height=1080,width=860,borderwidth=10,relief=tk.RIDGE) # input frame, 180,1600

    dframe_l.pack_propagate(False)
    dframe_l.pack(side='left')
    dframe_r.pack_propagate(False)
    dframe_r.pack(side='left')

    iframe.pack_propagate(False)
    iframe.pack(side='right')

    # Display Frame - Showing Images
        # Image - change image on click
    img = Is.getImage()
    img_label = tk.Label(dframe_l,image=img)
    img_label.pack()
    # img_label.grid(row=0,column=0)



    # Click events
        # Image - change on click, depending on prev/next
        # Submit - append name, and text boxes to .csv
    # Display Images
    l_img = tk.Label(dframe_l,text=Is.file_name)
    r_img = tk.Label(dframe_r,text=Is.file_name)
    l_img.pack(side='top')
    r_img.pack(side='top')

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
