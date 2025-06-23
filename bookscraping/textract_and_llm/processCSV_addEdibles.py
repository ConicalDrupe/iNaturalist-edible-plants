import os
import boto3
import json
import time
import pandas as pd
from llm_utils import call_mistral_7b

back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
df = pd.read_csv(os.path.join(back_dir,'outputs','txt_extract.csv'))

df['Mistral_edibles']=''
for idx,row in df.iterrows():
    food_data= ''.join(list(row.iloc[2]))

    prompt = f"""
    You are an expert in data cleaning and natural language processing, specializing in extracting edibile plant parts from unstructured text.

    Your task is to extract a one or several edible parts named from the given text. Each edible part consists of exactly one word. Ignore any extra words, punctuation, or formatting issues.

    Respond only with a list of edible parts. nothing else—no explanations, no additional text.

    Example input 1:
    'FOOD USE: The grain is gathered in early to mid summer by beating the heads into a bin or basket, or bys
    tripping the tops by hand. Dark, plump seeds are good; empties are smaller and light brown. Parch to bur
    noff the fluff, then rub and winnow to purify the seed (see p. 27). Conservation 1.'

    Expected output 1:
    'seeds'

    Example input 2:
    'FOOD USE: Gather berries from the branches by hand or shake them onto a tarp or cloth. They can be dried
    ,eaten fresh, or used in jams, jellies, pies, juice, or ice cream. Young leaves, especially on stump spr
    outs, can beeaten as a cooked green and have been traditionally dried and powdered as a flour additive. 
    Note: the warningssometimes seen about mulberry sap being hallucinogenic seem overblown and irrelevant t
    o normal food use.

    Expected output 2:
    'berries','Young leaves'


    Input:\n
    {food_data}

    Output:
    """

    time.sleep(0.5)
    llm_res = call_mistral_7b(prompt)
    df.loc[idx,'Mistral_edibles'] = llm_res
    print('succeeded matching ',idx)


one_dir_back = os.path.normpath(os.getcwd() + os.sep + os.pardir)
df.to_csv(os.path.join(one_dir_back,'outputs','mistral_appended_edibles.csv'),index=False)
