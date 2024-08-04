
import pandas as pd
import os


back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
two_back_dir = os.path.normpath(back_dir + os.sep + os.pardir)
api_output_dir = os.path.join(two_back_dir,'data','outputs','api')

master = pd.DataFrame()
for file in os.listdir(api_output_dir):
  df = pd.read_csv(os.path.join(api_output_dir,file))
  master = pd.concat([master,df])

print(master.columns)
print(master.shape)
print(master['Genus'].nunique())
print(master['Species Name'].nunique())
print(master['nubKey'].nunique())

master.to_csv(os.path.join(two_back_dir,'data','outputs','all_genera_to_species.csv'),index=False)
