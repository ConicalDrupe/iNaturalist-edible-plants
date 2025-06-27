import tkinter as tk
from tkinter import ttk
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
    
    # Create two separate ImageState objects
    Is_left = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/', filter_ls=file_filter, debug_mode=True)
    Is_right = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/', filter_ls=file_filter, debug_mode=True)
    Is_right.next()  # Right image is one ahead
    
    Ts = TextState(txt_path=os.path.join(back_dir, 'outputs', 'txt_files'), filter_ls=file_filter, debug_mode=True)

    window = tk.Tk()
    session_id = uuid.uuid4()
    window.geometry('1920x1080')
    window.title("Data Verifier")
    window.configure(bg='#f0f0f0')

    # Main container frame
    main_frame = tk.Frame(window, bg='#f0f0f0')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Left side - Images display
    images_container = tk.Frame(main_frame, bg='#f0f0f0')
    images_container.pack(side='left', fill='both', expand=True, padx=(0, 10))

    # Left image frame with title
    left_container = tk.Frame(images_container, bg='#f0f0f0')
    left_container.pack(side='left', fill='both', expand=True, padx=(0, 5))
    
    left_title = tk.Label(left_container, text=Is_left.file_name, font=('Arial', 12, 'bold'), 
                         bg='#f0f0f0', fg='#2c3e50')
    left_title.pack(pady=(0, 10))
    
    dframe_l = tk.Frame(left_container, height=800, width=400, borderwidth=2, 
                       relief=tk.RIDGE, bg='white')
    dframe_l.pack_propagate(False)
    dframe_l.pack(fill='both', expand=True)

    # Right image frame with title
    right_container = tk.Frame(images_container, bg='#f0f0f0')
    right_container.pack(side='right', fill='both', expand=True, padx=(5, 0))
    
    right_title = tk.Label(right_container, text=Is_right.file_name, font=('Arial', 12, 'bold'), 
                          bg='#f0f0f0', fg='#2c3e50')
    right_title.pack(pady=(0, 10))
    
    dframe_r = tk.Frame(right_container, height=800, width=400, borderwidth=2, 
                       relief=tk.RIDGE, bg='white')
    dframe_r.pack_propagate(False)
    dframe_r.pack(fill='both', expand=True)

    # Right side - Input frame
    iframe = tk.Frame(main_frame, height=1080, width=350, borderwidth=2, 
                     relief=tk.RIDGE, bg='#ffffff', padx=20, pady=20)
    iframe.pack_propagate(False)
    iframe.pack(side='right', fill='y')

    # Display Images
    img_left = Is_left.getImage()
    img_label_left = tk.Label(dframe_l, image=img_left, bg='white')
    img_label_left.pack(expand=True)

    img_right = Is_right.getImage()
    img_label_right = tk.Label(dframe_r, image=img_right, bg='white')
    img_label_right.pack(expand=True)

    # Text display area
    text_frame = tk.LabelFrame(iframe, text="Extracted Text", font=('Arial', 10, 'bold'), 
                              bg='#ffffff', fg='#2c3e50', padx=10, pady=10)
    text_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 20))
    
    txt = Ts.getText()
    txt_label = tk.Label(text_frame, text=txt[:200] + "..." if len(txt) > 200 else txt, 
                        wraplength=300, justify='left', bg='#ffffff', fg='#34495e')
    txt_label.pack()

    # Input section
    input_frame = tk.LabelFrame(iframe, text="Manual Corrections", font=('Arial', 10, 'bold'), 
                               bg='#ffffff', fg='#2c3e50', padx=10, pady=10)
    input_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 20))

    # Species entry
    tk.Label(input_frame, text='Species:', font=('Arial', 9), bg='#ffffff', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
    species_box = tk.Entry(input_frame, width=25, font=('Arial', 9))
    species_box.grid(row=0, column=1, columnspan=2, sticky='ew', padx=(10, 0), pady=5)

    # Edible parts entry
    tk.Label(input_frame, text='Edible Parts:', font=('Arial', 9), bg='#ffffff', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
    edible_box = tk.Entry(input_frame, width=25, font=('Arial', 9))
    edible_box.grid(row=1, column=1, columnspan=2, sticky='ew', padx=(10, 0), pady=5)

    # Checkboxes section
    checkbox_frame = tk.LabelFrame(iframe, text="Additional Options", font=('Arial', 10, 'bold'), 
                                  bg='#ffffff', fg='#2c3e50', padx=10, pady=10)
    checkbox_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 20))

    multiple_species = tk.IntVar()
    several_pages = tk.IntVar()
    unused = tk.IntVar()

    cbox_multiple_species = tk.Checkbutton(checkbox_frame, text="Multiple species", 
                                         variable=multiple_species, onvalue=1, offvalue=0,
                                         bg='#ffffff', fg='#2c3e50', font=('Arial', 9))
    cbox_multiple_species.grid(row=0, column=0, sticky='w', pady=2)

    cbox_several_pages = tk.Checkbutton(checkbox_frame, text="Spans several pages", 
                                      variable=several_pages, onvalue=1, offvalue=0,
                                      bg='#ffffff', fg='#2c3e50', font=('Arial', 9))
    cbox_several_pages.grid(row=1, column=0, sticky='w', pady=2)

    cbox_unused = tk.Checkbutton(checkbox_frame, text="Unused page", 
                               variable=unused, onvalue=1, offvalue=0,
                               bg='#ffffff', fg='#2c3e50', font=('Arial', 9))
    cbox_unused.grid(row=2, column=0, sticky='w', pady=2)

    # Configure grid weights for input_frame
    input_frame.columnconfigure(1, weight=1)
    checkbox_frame.columnconfigure(0, weight=1)

    # Functions
    def update():
        # Update Left Image Display
        img_left = Is_left.getImage()
        img_label_left.config(image=img_left)
        img_label_left.image = img_left
        left_title.config(text=Is_left.file_name)

        # Update Right Image Display
        img_right = Is_right.getImage()
        img_label_right.config(image=img_right)
        img_label_right.image = img_right
        right_title.config(text=Is_right.file_name)

        # Update Text Display
        txt = Ts.getText()
        display_txt = txt[:200] + "..." if len(txt) > 200 else txt
        txt_label.config(text=display_txt)

        # Clear Text Boxes
        species_box.delete(0, tk.END)
        edible_box.delete(0, tk.END)

        # Clear Check Boxes
        multiple_species.set(0)
        several_pages.set(0)
        unused.set(0)

    def next():
        Is_left.next()
        Is_right.next()
        Ts.next()
        update()

    def prev():
        Is_left.prev()
        Is_right.prev()
        Ts.prev()
        update()

    def submit_click():
        # Checking source name
        source = Is_left.file_name
        if '.' in source:
            source = source.split('.')[0]

        # Creating data string
        # SCHEMA: source | name_data | food_data | multiple_species | several_pages | unused
        data = [source, species_box.get(), edible_box.get(), 
                multiple_species.get(), several_pages.get(), unused.get()]

        # Setting up csv path, write/append mode, and writer
        back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        output_csv = os.path.join(back_dir, 'outputs', 'gui', f'{session_id}.csv')
        csv_mode = 'w' if not os.path.exists(output_csv) else 'a'

        with open(output_csv, csv_mode) as file:
            writer = csv.writer(file)
            writer.writerow(data)

        # Visual feedback
        submit_button.config(text="Submitted!", bg='#27ae60')
        window.after(1000, lambda: submit_button.config(text="Submit", bg='#3498db'))

    # Buttons section
    button_frame = tk.Frame(iframe, bg='#ffffff')
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    # Style buttons
    button_style = {'font': ('Arial', 10, 'bold'), 'width': 8, 'height': 2, 'relief': tk.RAISED, 'bd': 2}

    prev_button = tk.Button(button_frame, text="◄ Prev", command=prev, 
                           bg='#e74c3c', fg='white', **button_style)
    prev_button.grid(row=0, column=0, padx=5)

    submit_button = tk.Button(button_frame, text="Submit", command=submit_click, 
                             bg='#3498db', fg='white', **button_style)
    submit_button.grid(row=0, column=1, padx=5)

    next_button = tk.Button(button_frame, text="Next ►", command=next, 
                           bg='#2ecc71', fg='white', **button_style)
    next_button.grid(row=0, column=2, padx=5)

    # Configure iframe grid weights
    iframe.grid_rowconfigure(0, weight=1)
    iframe.grid_rowconfigure(1, weight=0)
    iframe.grid_rowconfigure(2, weight=0)
    iframe.grid_rowconfigure(3, weight=0)
    iframe.grid_columnconfigure(0, weight=1)

    window.mainloop()


if __name__ == "__main__":
    # Creating filter list
    import pandas as pd
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    df = pd.read_csv(os.path.join(back_dir, 'outputs', 'txt_extract.csv'))
    df = df[df['found_edibilty'] == False]
    filter_ls = df['source'].map(lambda x: x.split('.')[0]).to_list()

    gui2(file_filter=None)
