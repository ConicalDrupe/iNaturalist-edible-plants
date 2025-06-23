import tkinter as tk
from PIL import ImageTk, Image
import os

class ImageDisplayer:

    def __init__(self,ImagePath='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/'):

        self.index = 0
        self.paths = getImageList(ImagePath)
        self.length = len(self.paths)

    def getImageName(self):
        return os.path.basename(self.paths[self.index]).split('.')[0]

    def currentImage(self):
        return getImage(self.paths[self.index])

    def nextImage(self):
        if self.index + 2 < self.length:
            self.index += 1
        else:
            print('At end of list')

    def prevImage(self):
        if self.index - 1 < 0:
            print('Cannot go back. Currently at end of the list')
        else:
            self.index -= 1


def getImageList(ImagePath='/mnt/c/Users/C/Documents/DataProjects2025/SamThayerScan_v2/Final Organized Photos/'):
    dir = [file for file in os.listdir(ImagePath) if file.endswith('.tif')]
    return [os.path.join(ImagePath,file) for file in dir]

def getImage(image_path,max_size=(1000,2000)):
    img = Image.open(image_path)
    img.thumbnail(max_size)
    return ImageTk.PhotoImage(img)

def create_gui():
    # img_ls = getImageList()
    ImD = ImageDisplayer()

    # Create the main window (root window)
    root = tk.Tk()
    root.title("Data Verifyer")  # Set the window title

    image = ImD.currentImage()
    # image_label = tk.Label(root, image =image)
    image_label=tk.Label(root,text=ImD.getImageName())
    image_label.pack()

    # # Create a Label widget
    # label = tk.Label(root, text=", Tkinter!")
    # label.pack(pady=20)  # Pack the label with some vertical padding
    #
    # # Create a Button widget
    next_button = tk.Button(root, text="Next", command=ImD.nextImage)
    next_button.pack()

    prev_button = tk.Button(root, text="Prev", command=ImD.prevImage)
    prev_button.pack()

    # Start the Tkinter event loop
    # This keeps the window open and responsive to user interactions
    root.mainloop()

if __name__ == "__main__":
    create_gui()
