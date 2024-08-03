import os
import re
import pandas as pd
from edible_hashmap_2 import edible_map
from ast import literal_eval


def read_southeast_raw(folder='outputs',file='southeast-foraging-rawdata.csv'):
    back_dir_one = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    back_dir = os.path.normpath(back_dir_one + os.sep + os.pardir) # two directories back
    dpath = os.path.join(back_dir,'data',folder,file)
    df = pd.read_csv(dpath)
    return df

def col_remove_whitespace(dataframe):
    df = dataframe.copy()
    # Clean White Spaces
    for col in df.columns:
      df[col] = df[col].str.strip()
      df[col] = df[col].replace('   ',' ')
      df[col] = df[col].replace('  ',' ')
      df[col] = df[col].str.strip()
    return df

def edible_column_cleaning(df):
    ed = df['Edible'].apply(lambda x: x.strip(',').split(','))

    # ed elements are list[str]
    # below cleans whitespace
    ed = ed.apply(lambda l:[x.strip() for x in l])
    return ed

def clean_initial_southeast():
    df = read_southeast_raw()
    df = col_remove_whitespace(df)
    df['Edible'] = edible_column_cleaning(df)
    print('Saving Initially Cleaned southeast-foraging-raw.csv')
    print('To staging as: southeast-foraging-clean_1.csv')
    df.to_csv('/home/boon/Projects/iNaturalist-edible-plants/data/staging/southeast-foraging-clean_1.csv',index=False)
    return

# Create New columns

def get_unique_edible_names(s):
  # Get series of unique edible parts
  s = s.apply(literal_eval) #ensure list gets evaluated as a list
  ed = pd.Series(s.explode().unique()).str.strip()
  # Remove young prefix and (nuts) post fix
  clean_ed = ed.str.replace('young ',' ').str.replace(' (acorns)',' ').str.strip()
  # Map names
  clean_ed = clean_ed.apply(lambda x: edible_map[x] if x in edible_map.keys() else x)
  # print(clean_ed)
  names = pd.Series(clean_ed.unique()).str.title().tolist() 
  return names

# Creating Indicator Matrix

def search_edible_and_map(df,ls,row_index,mapping=edible_map):
  edible_columns = pd.Series(mapping.values()).str.title()
  values = edible_columns.copy().str.lower()

  for item in ls:
    for edible in edible_columns:
      match = re.search(edible,item) #searches list item for containment of edible
      if match:
        df.iloc[row_index,edible] = 1
  return df.copy()

def create_indicator_matrix(dataframe,mapping=edible_map):
    # Requires cleaned ['Edible'] column within dataframe 
    df = dataframe.copy()
    names = get_unique_edible_names(df['Edible'])
    # Create new columns
    for name in names:
        df[name] = 0

    # Search and flag Edible Category key in ['Edible'] column
    for index,value in df['Edible'].items():
        search_edible_and_map(value,index)

    return df

def create_indicator_matrix_via_proxy(df,mapping=edible_map):
    df['temp'] = df['Edible']
    df['temp'] = df['temp'].apply(literal_eval)

    df['temp'] = df['temp'].apply(lambda l: [x.replace('young ','').strip() for x in l])
    df['temp'] = df['temp'].apply(lambda l: [x.replace(' (acorns)',' ').strip() for x in l])
    df['temp'] = df['temp'].apply(lambda l: [mapping[x] if x in list(mapping.keys()) else x for x in l])

    names = get_unique_edible_names(df['Edible'])
    for name in names:
      df[name] = 0

    cols = names.copy()
    cols.append('Edible')

    for index, value in df['temp'].items():
      for val in value:
        for name in names:
          match = re.search(name,val,re.IGNORECASE)
          if match:
            df.loc[index,name] = 1

    df = df.rename(columns={'Nut':'Nuts','Leave':'Leaves','Seed':'Seeds','Fruit':'Fruits','Flower':'Flowers','Shoot':'Shoots','Bud':'Flower Buds','Twig':'Twigs','Needle':'Needles'})
    df = df.drop(['Edible','When and Where','temp'],axis=1)
    return df


def clean_second_southeast():
    df = read_southeast_raw(folder='staging',file='southeast-foraging-clean_1.csv')
    df = create_indicator_matrix_via_proxy(df)
    print('Saving Second Cleaned southeast-foraging-clean_1.csv')
    print('To staging as: southeast-foraging-clean_IM.csv')
    df.to_csv('/home/boon/Projects/iNaturalist-edible-plants/data/staging/southeast-foraging-clean_IM.csv',index=False)
    return

if __name__ == "__main__":
    # Initial cleaning of whitespace
    clean_initial_southeast()

    # Creating Indicator matrix of edible parts of each plant
    clean_second_southeast()

