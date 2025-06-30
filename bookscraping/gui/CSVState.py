import os
import pandas as pd

class CSVState:
    def __init__(self,csv_path,edible_col,name_col,source_col='source',filter_ls=None,debug_mode=False):
        self.index=0
        self.edible_col = edible_col
        self.name_col = name_col
        self.source_col = source_col

        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.length = self.df.shape[0]

        self.debug_mode=debug_mode

        # Filter out
        if filter_ls:
            self.df = self.df.iloc[~self.df[self.source_col].isin(filter_ls).index]

    def updateName(self):
        self.source_name = self.df.loc[self.index,self.source_col]

        if self.debug_mode:
            print('Name Updated! ',self.source_name)
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

    def getName(self):
        text_data = self.df.loc[self.index,self.name_col]
        return text_data

    def getEdible(self):
        text_data = self.df.loc[self.index,self.edible_col]
        return text_data
