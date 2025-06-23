import os
import pandas as pd

class ExtractDisplay:

    def __init__(self,csv_path):
        df = pd.read_csv(csv_path)
        df['source'] = df['source'].map(lambda x: x.split('.')[0]) #splitting out extension
        self.df = df


    def getName(self,name):

        if '.' in name:
            name = name.split('.')[0]

        return ''.join(self.df[self.df['source']==name]['name_data'].values)

    def getEdible(self,name):

        if '.' in name:
            name = name.split('.')[0]

        return ''.join(self.df[self.df['source']==name]['food_data'].values)

if __name__ == "__main__":
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)

    ED = ExtractDisplay(csv_path=os.path.join(back_dir,'outputs','txt_extract.csv'))

    t = ED.getEdible('0001_a')
    # t = ED.getName('0001_a')
    print(t)

