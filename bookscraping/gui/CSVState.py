import os
import pandas as pd

class CSVState:
    def __init__(self,csv_path,edible_col,name_col,image_name_ls,source_col='source',filter_ls=None,debug_mode=False):
        self.index=0
        self.edible_col = edible_col
        self.name_col = name_col
        self.source_col = source_col

        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.df = self.df[[self.source_col,self.name_col,self.edible_col]]
        self.length = self.df.shape[0]

        self.debug_mode=debug_mode

        # Adding extra rows for image sources not in csv
        csv_sources = self.df[self.source_col].unique()
        # Ensure cleaning of image_name_ls
        def process_image_path(img_path):
            return os.path.basename(img_path).split('.')[0] if '.' in img_path else img_path

        image_name_ls = [process_image_path(img) for img in image_name_ls]
        sources_to_append = [source for source in image_name_ls if source not in csv_sources]
        fillers = ['Enter Manually' for i in range(len(sources_to_append))]
        append_df = pd.DataFrame({self.source_col:sources_to_append,self.name_col:fillers,self.edible_col:fillers})
        self.df = pd.concat([self.df,append_df])

        # Filter out
        if filter_ls:
            self.df = self.df[~self.df[self.source_col].isin(filter_ls)]

        # Sort Values and reset index
        self.df = self.df.sort_values(self.source_col,ascending=True)
        self.df.reset_index(drop=True,inplace=True)

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

    def getPage(self):
        page_data = self.df.loc[self.index,self.source_col]
        return page_data

    def jumpTo(self,name):
        name = name.strip()
        if name not in self.df[self.source_col].unique():
            print(rf"[ERROR] CSVState has no image name {name}")
            print(name)
            return 0
        else:
            idx = self.df[self.df[self.source_col]==name].index
            self.index = idx
            self.updateName()
            return 1


