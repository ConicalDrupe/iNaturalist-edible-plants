
import os
import pandas as pd
from llm_utils import call_mistral_7b

df = pd.read_csv(os.path.join(os.getcwd(),'book_extract.csv'))

matched = df[df['found_edibilty']==True].reset_index(drop=True)

matched['Mistral_scientific_name']=''
for idx,row in matched.iterrows():
    name_data= ''.join(list(row.iloc[1]))

    prompt = f"""
    You are an expert in data cleaning and natural language processing, specializing in extracting scientific names from unstructured text.

    Your task is to extract a single binomial scientific name from the given text. The scientific name consists of exactly two words: the genus and species. Ignore any extra words, punctuation, or formatting issues.

    Respond only with the two-word scientific name and nothing else—no explanations, no additional text.

    Example input:
    ['NEEDLE-LEAVED TREES AND SHRUBS', '3 Balsam fir', 'Abies balsmaea Pinacea (Pine family)']

    Expected output:
    Abies balsmaea

    Input:\n
    {name_data}

    Output:
    """

    llm_res = call_mistral_7b(prompt)
    matched.loc[idx,'Mistral_scientific_name'] = llm_res

matched.to_csv(os.path.join(os.getcwd(),'matched_311_mistral_names.csv'),index=False)
