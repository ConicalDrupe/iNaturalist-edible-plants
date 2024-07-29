# Common Name
# Species Name
# Edible
# When and Where

# Dictionary Keys:
    # Plant_Number:
        # Common Name
        # Species Name
        # Edible
        # When and Where
        
# Page number is an indicator for Common Name
# Between common name and EDIBLE is the scientific name (Only require two strings for scientific name)
# Proceeding after EDIBLE is edibility info #stops at next capitol letter
# Search for Where and When to Gather
# Stopping condition is How to Gather - Ignore page changes in search and stop

import json
import pandas as pd
import re
import os

raw_path = os.path.join(os.getcwd(),'~/Projects/iNaturalist-edible-plants/data/outputs/southeast_foraging.json')

with open(raw_path) as json_file:
    data = json.load(json_file)


# extract all text content
pages = data["pages"]
extracted_content = []
for page in pages:
    for content in page["text_content"]:
        extracted_content.append(content)

#%%
# clean font size
for line in extracted_content:
    line["font_size"] = round(line["font_size"])
#%%

# Extract text in ordered fashion: Does not proceed until entire dict for a 
# plan is filled

# initialize master dictionary
plant_info = {"Common Name" : [], 
              "Scientific Name" : [],
              "Edible" : [],
              "When and Where" : []}
master = {}
i=0
master[i] = plant_info

# initialize logic flags, gates control whether to move onto next plant value
flag1=0
flag2=0
flag3=0

for line in extracted_content:
    # Extract common name based on fontsize
    if line["font_size"] == 30:
        master[i]["Common Name"] = line["text"]
        flag1 = 1
    # Extract Scientific name, always comes directly after Common Name
    if flag1 and line["font_size"] == 17:
        master[i]["Scientific Name"] = line["text"]
        flag1 = 0
    # If previous line was EDIBLE then extract this text
    if flag2:
        master[i]["Edible"] = line["text"]
        flag2 = 0
    # Flags if current line is EDIBLE
    if line["text"] == "EDIBLE":
        flag2 = 1
    # Flags if current line is Where and When to Gather
    if line["text"] == "Where and When to Gather":
        flag3 = 1
        wandw = ""
    # If flagged, we are contuniously extracting text, until we hit end flag
    if flag3:
        wandw = wandw + " " + line["text"]
        if line["text"] == "How to Gather":
            master[i]["When and Where"] = wandw
            flag3 = 0 
    
    if all(master[i].values()) and flag3==0:
        print("Moving to Next Plant...")
        i+=1
        plant_info = {"Common Name" : [], 
                      "Scientific Name" : [],
                      "Edible" : [],
                      "When and Where" : []}
        master[i] = plant_info
        
#%%
# stor in dataframe
df = pd.DataFrame.from_dict(master, orient='index')

#%%
# stripping white space left and right

for column in df.columns:
    df[f"{column}"] = df[f"{column}"].str.lstrip()
    df[f"{column}"] = df[f"{column}"].str.rstrip()

# capitalize first letter in common name
df['Common Name'] = df['Common Name'].str.capitalize()
    
# Removing "Where and When to Gather" and "How to Gather"
# The first is 25 characters, while the last is 14 characters (including spaces)
df["When and Where"] = df["When and Where"].str[25:-14]

# drop last row "Acknowledgements"
df = df.iloc[:-1]

# save as csv
direct = '~/Projects/iNaturalist-edible-plants/data/outputs/southeast-foraging-rawdata.csv'
df.to_csv(direct)
