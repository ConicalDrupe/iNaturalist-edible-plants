import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import ImageTk, Image
import os
import csv
import uuid
from CSVState import CSVState
from ImageState import ImageState


def gui(file_filter=None):
    # Need something that manages program state!
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    
    # Create two separate ImageState objects
    Is_left = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/', filter_ls=file_filter, debug_mode=True)
    Is_right = ImageState(image_path='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/', filter_ls=file_filter, debug_mode=True)
    Is_left.prev()  # Left image is one behind
    
    Ts = CSVState(csv_path=os.path.join(back_dir, 'outputs','reprocessing','final_to_review_2.csv'), filter_ls=file_filter,edible_col='edibles',name_col='cleaned_names',image_name_ls=Is_left.image_ls,debug_mode=True)

    window = tk.Tk()
    session_id = uuid.uuid4()
    window.geometry('1920x1080')
    window.title("Data Verifier - Botanical Scanner")
    window.configure(bg='#f8fafc')
    
    # Configure window to be resizable
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Main container frame with improved styling
    main_frame = tk.Frame(window, bg='#f8fafc')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Left side - Images display (reduced width to give more space to text panel)
    images_container = tk.Frame(main_frame, bg='#f8fafc')
    images_container.pack(side='left', fill='both', expand=True, padx=(0, 20))

    # Left image frame with enhanced styling
    left_container = tk.Frame(images_container, bg='#f8fafc')
    left_container.pack(side='left', fill='both', expand=True, padx=(0, 10))
    
    left_title = tk.Label(left_container, text=Is_left.file_name, font=('Segoe UI', 14, 'bold'), 
                         bg='#f8fafc', fg='#1e293b')
    left_title.pack(pady=(0, 15))
    
    # Enhanced frame styling with subtle shadow effect
    dframe_l = tk.Frame(left_container, height=800, width=400, borderwidth=0, 
                       relief=tk.FLAT, bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=2)
    dframe_l.pack_propagate(False)
    dframe_l.pack(fill='both', expand=True)

    # Right image frame with enhanced styling
    right_container = tk.Frame(images_container, bg='#f8fafc')
    right_container.pack(side='right', fill='both', expand=True, padx=(10, 0))
    
    right_title = tk.Label(right_container, text=Is_right.file_name, font=('Segoe UI', 14, 'bold'), 
                          bg='#f8fafc', fg='#1e293b')
    right_title.pack(pady=(0, 15))
    
    dframe_r = tk.Frame(right_container, height=800, width=400, borderwidth=0, 
                       relief=tk.FLAT, bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=2)
    dframe_r.pack_propagate(False)
    dframe_r.pack(fill='both', expand=True)

    # Right side - Input frame (increased width and improved styling)
    iframe = tk.Frame(main_frame, height=1080, width=450, borderwidth=0, 
                     relief=tk.FLAT, bg='#ffffff', padx=30, pady=30,
                     highlightbackground='#e2e8f0', highlightthickness=2)
    iframe.pack_propagate(False)
    iframe.pack(side='right', fill='y')

    # Display Images
    img_left = Is_left.getImage()
    img_label_left = tk.Label(dframe_l, image=img_left, bg='#ffffff')
    img_label_left.pack(expand=True)

    img_right = Is_right.getImage()
    img_label_right = tk.Label(dframe_r, image=img_right, bg='#ffffff')
    img_label_right.pack(expand=True)

    # NEW: Search section at the top of iframe
    search_frame = tk.LabelFrame(iframe, text="Search by Name", font=('Segoe UI', 12, 'bold'), 
                                bg='#ffffff', fg='#1e293b', padx=20, pady=15,
                                borderwidth=2, relief=tk.GROOVE)
    search_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 25))

    # Search entry box
    search_box = tk.Entry(search_frame, width=25, font=('Segoe UI', 12),
                         borderwidth=2, relief=tk.GROOVE, bg='#f9fafb',
                         highlightbackground='#d1d5db', highlightthickness=1)
    search_box.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(0, 10))

    # Search button
    search_button = tk.Button(search_frame, text="Search", font=('Segoe UI', 11, 'bold'),
                             bg='#6366f1', fg='white', activebackground='#4f46e5',
                             relief=tk.FLAT, bd=0, cursor='hand2', width=8)
    search_button.grid(row=0, column=1, pady=(0, 10))

    # Error message label (initially hidden)
    search_message = tk.Label(search_frame, text="", font=('Segoe UI', 10),
                             bg='#ffffff', fg='#ef4444')
    search_message.grid(row=1, column=0, columnspan=2, sticky='w', pady=(5, 0))

    # Configure search frame grid weights
    search_frame.columnconfigure(0, weight=1)

    # Enhanced text display area
    text_frame = tk.LabelFrame(iframe, text="Extracted Text", font=('Segoe UI', 12, 'bold'), 
                              bg='#ffffff', fg='#1e293b', padx=20, pady=15,
                              borderwidth=2, relief=tk.GROOVE)
    text_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 25))
    
    edible_txt = Ts.getEdible()
    name_txt = Ts.getName()
    page_name = Ts.getPage()
    
    def createLabelText(name_txt, edible_txt, page_name):
        # Extract actual values if they are pandas Series
        if hasattr(name_txt, 'iloc'):  # Check if it's a pandas Series
            name_txt = name_txt.iloc[0] if len(name_txt) > 0 else str(name_txt)
        if hasattr(edible_txt, 'iloc'):  # Check if it's a pandas Series
            edible_txt = edible_txt.iloc[0] if len(edible_txt) > 0 else str(edible_txt)
        if hasattr(page_name, 'iloc'):  # Check if it's a pandas Series
            page_name = page_name.iloc[0] if len(page_name) > 0 else str(page_name)
        
        # Convert to strings and truncate if necessary
        name_txt = str(name_txt)
        edible_txt = str(edible_txt)
        page_name = str(page_name)
        
        if len(name_txt) > 300:
            name_txt = name_txt[:150] + '...'
        if len(edible_txt) > 300:
            edible_txt = edible_txt[:150] + '...'

        formatted_text = f"PAGE: {page_name}\n\n" + "NAME:\n" + name_txt + "\n\n" + "EDIBLES:\n" + edible_txt
        return formatted_text

    # Enhanced text label with better formatting
    txt_label = tk.Label(text_frame, text=createLabelText(name_txt, edible_txt, page_name),
                        wraplength=380, justify='left', bg='#ffffff', fg='#374151',
                        font=('Segoe UI', 11), pady=10)
    txt_label.pack(fill='x')

    # Enhanced input section
    input_frame = tk.LabelFrame(iframe, text="Manual Corrections", font=('Segoe UI', 12, 'bold'), 
                               bg='#ffffff', fg='#1e293b', padx=20, pady=15,
                               borderwidth=2, relief=tk.GROOVE)
    input_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 25))

    # Enhanced species entry
    tk.Label(input_frame, text='Species:', font=('Segoe UI', 11, 'bold'), 
             bg='#ffffff', fg='#374151').grid(row=0, column=0, sticky='w', pady=(0, 15))
    species_box = tk.Entry(input_frame, width=30, font=('Segoe UI', 12),
                          borderwidth=2, relief=tk.GROOVE, bg='#f9fafb',
                          highlightbackground='#d1d5db', highlightthickness=1)
    species_box.grid(row=0, column=1, columnspan=2, sticky='ew', padx=(15, 0), pady=(0, 15))

    # Enhanced edible parts entry
    tk.Label(input_frame, text='Edible Parts:', font=('Segoe UI', 11, 'bold'), 
             bg='#ffffff', fg='#374151').grid(row=1, column=0, sticky='w', pady=(0, 15))
    edible_box = tk.Entry(input_frame, width=30, font=('Segoe UI', 12),
                         borderwidth=2, relief=tk.GROOVE, bg='#f9fafb',
                         highlightbackground='#d1d5db', highlightthickness=1)
    edible_box.grid(row=1, column=1, columnspan=2, sticky='ew', padx=(15, 0), pady=(0, 15))

    # Enhanced checkboxes section
    checkbox_frame = tk.LabelFrame(iframe, text="Additional Options", font=('Segoe UI', 12, 'bold'), 
                                  bg='#ffffff', fg='#1e293b', padx=20, pady=15,
                                  borderwidth=2, relief=tk.GROOVE)
    checkbox_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 30))

    multiple_species = tk.IntVar()
    several_pages = tk.IntVar()
    unused = tk.IntVar()

    # Enhanced checkboxes with better styling
    cbox_multiple_species = tk.Checkbutton(checkbox_frame, text="Multiple species", 
                                         variable=multiple_species, onvalue=1, offvalue=0,
                                         bg='#ffffff', fg='#374151', font=('Segoe UI', 11),
                                         activebackground='#f3f4f6', selectcolor='#ffffff')
    cbox_multiple_species.grid(row=0, column=0, sticky='w', pady=8)

    cbox_several_pages = tk.Checkbutton(checkbox_frame, text="Spans several pages", 
                                      variable=several_pages, onvalue=1, offvalue=0,
                                      bg='#ffffff', fg='#374151', font=('Segoe UI', 11),
                                      activebackground='#f3f4f6', selectcolor='#ffffff')
    cbox_several_pages.grid(row=1, column=0, sticky='w', pady=8)

    cbox_unused = tk.Checkbutton(checkbox_frame, text="Unused page", 
                               variable=unused, onvalue=1, offvalue=0,
                               bg='#ffffff', fg='#374151', font=('Segoe UI', 11),
                               activebackground='#f3f4f6', selectcolor='#ffffff')
    cbox_unused.grid(row=2, column=0, sticky='w', pady=8)

    # Configure grid weights for better layout
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
        name_txt = Ts.getName()
        edible_txt = Ts.getEdible()
        page_name = Ts.getPage()
        display_txt = createLabelText(name_txt, edible_txt, page_name) 
        txt_label.config(text=display_txt)

        # Clear Text Boxes
        species_box.delete(0, tk.END)
        edible_box.delete(0, tk.END)

        # Clear Check Boxes
        multiple_species.set(0)
        several_pages.set(0)
        unused.set(0)

    # NEW: Search function
    def search_name():
        search_term = search_box.get().strip()
        if not search_term:
            return
        
        # Try to jump to the specified name in both ImageState objects and CSVState
        left_result = Is_left.jumpTo(search_term)
        if left_result:
            Is_left.prev()
        right_result = Is_right.jumpTo(search_term)
        csv_result = Ts.jumpTo(search_term)
        
        # Check if search was successful (1 = found, 0 = not found)
        if left_result == 1 and right_result == 1 and csv_result == 1:
            # Success - change search box to green and clear any error message
            search_box.config(bg='#dcfce7', highlightbackground='#16a34a')  # Light green background
            search_message.config(text="", fg='#16a34a')
            # Update the display to show the found data
            update()
        else:
            # Failure - change search box to red and show error message
            search_box.config(bg='#fef2f2', highlightbackground='#dc2626')  # Light red background
            search_message.config(text=f"Image with name '{search_term}' not found", fg='#dc2626')

    def reset_search_box():
        # Reset search box appearance when user starts typing
        search_box.config(bg='#f9fafb', highlightbackground='#d1d5db')
        search_message.config(text="")

    # Bind search functionality
    search_button.config(command=search_name)
    search_box.bind('<Return>', lambda event: search_name())
    search_box.bind('<KeyPress>', lambda event: window.after(1, reset_search_box))

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
        l_source = Is_left.file_name
        r_source = Is_right.file_name
        if '.' in l_source:
            l_source = l_source.split('.')[0]
        if '.' in r_source:
            r_source = r_source.split('.')[0]

        # Creating data string
        # SCHEMA: source | name_data | food_data | multiple_species | several_pages | unused
        data = [l_source, r_source, species_box.get(), edible_box.get(), 
                multiple_species.get(), several_pages.get(), unused.get()]

        # Setting up csv path, write/append mode, and writer
        back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        output_csv = os.path.join(back_dir, 'outputs', 'gui', f'{session_id}.csv')
        csv_mode = 'w' if not os.path.exists(output_csv) else 'a'

        with open(output_csv, csv_mode) as file:
            writer = csv.writer(file)
            writer.writerow(data)

        # Submition moves us to next page
        next()

    # Keyboard event handlers
    def on_key_press(event):
        # Check if focus is on an Entry widget to avoid interfering with text input
        focused_widget = window.focus_get()
        if isinstance(focused_widget, tk.Entry):
            return
        
        if event.keysym == 'Left':
            prev()
        elif event.keysym == 'Right':
            next()
        elif event.keysym == 'Return':
            submit_click()
    # Bind keyboard shortcuts to the window
    window.bind('<Key>', on_key_press)
    window.focus_set()  # Ensure window can receive keyboard event
    # Enhanced buttons section
    button_frame = tk.Frame(iframe, bg='#ffffff')
    button_frame.grid(row=4, column=0, columnspan=3, pady=30)

    # Enhanced button styling with modern design
    button_style = {
        'font': ('Segoe UI', 12, 'bold'), 
        'width': 10, 
        'height': 2, 
        'relief': tk.FLAT, 
        'bd': 0,
        'cursor': 'hand2'
    }

    prev_button = tk.Button(button_frame, text="◄ Previous", command=prev, 
                           bg='#ef4444', fg='white', activebackground='#dc2626', **button_style)
    prev_button.grid(row=0, column=0, padx=8)

    next_button = tk.Button(button_frame, text="Next ►", command=next, 
                           bg='#10b981', fg='white', activebackground='#059669', **button_style)
    next_button.grid(row=0, column=1, padx=8)

    submit_button = tk.Button(button_frame, text="Submit", command=submit_click, 
                             bg='#3b82f6', fg='white', activebackground='#2563eb', **button_style)
    submit_button.grid(row=0, column=2, padx=8)
    # Key binds to text boxe
    species_box.bind('<Return>', lambda event: submit_click())
    edible_box.bind('<Return>', lambda event: submit_click())
    species_box.bind('<Right>', lambda event: next())
    edible_box.bind('<Right>', lambda event: next())
    species_box.bind('<Left>', lambda event: prev())
    edible_box.bind('<Left>', lambda event: prev())

    # Configure iframe grid weights for proper scaling
    iframe.grid_rowconfigure(0, weight=0)  # Search frame - fixed size
    iframe.grid_rowconfigure(1, weight=1)  # Text frame - expandable
    iframe.grid_rowconfigure(2, weight=0)  # Input frame - fixed size
    iframe.grid_rowconfigure(3, weight=0)  # Checkbox frame - fixed size
    iframe.grid_rowconfigure(4, weight=0)  # Button frame - fixed size
    iframe.grid_columnconfigure(0, weight=1)

    window.mainloop()


if __name__ == "__main__":
    # Creating filter list
    import pandas as pd
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    # filter_ls = []
    with open(os.path.join(back_dir, 'outputs','reprocessing','unused_pages_list.txt'),'r') as f:
        content = f.read()
        filter_ls = content.split('\n')

    gui(file_filter=filter_ls)
