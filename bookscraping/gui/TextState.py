import os

class TextState:
    def __init__(self,txt_path,filter_ls=None,debug_mode=False):
        self.index=0
        if filter_ls:
            self.txt_ls = [os.path.join(txt_path,file) for file in os.listdir(txt_path) if file.endswith('.txt') and file.split('.')[0] not in filter_ls]
        else:
            self.txt_ls = [os.path.join(txt_path,file) for file in os.listdir(txt_path) if file.endswith('.txt')]
        self.txt_ls.sort()
        self.txt_path=self.txt_ls[self.index]
        self.length = len(self.txt_ls)
        self.file_name = os.path.splitext(os.path.basename(self.txt_path[self.index]))[0]
        self.debug_mode=debug_mode


    def setLabel(self,label):
        self.label = label
        return

    def updateName(self):
        file = self.txt_ls[self.index]
        self.txt_path = file
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

    def getText(self):
        with open(self.txt_path,'r') as file:
            text_data = file.read()
        return text_data
