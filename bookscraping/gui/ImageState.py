import os
from PIL import ImageTk, Image

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
