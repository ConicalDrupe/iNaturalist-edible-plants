
import os
import boto3
import json
import time
import pandas as pd

df = pd.read_csv(os.path.join(os.getcwd(),'matched_311_mistral_names.csv'))


def call_mistral_7b(prompt,  max_tokens=1000, temperature=0.7,retries=5, backoff_factor=2):
    """
    Calls Mistral-7B on AWS Bedrock using Boto3.
    
    :param prompt: Input text prompt for the model.
    :param model_id: The model ID for Mistral-7B on AWS Bedrock.
    :param max_tokens: Maximum number of tokens to generate.
    :param temperature: Sampling temperature (higher values = more randomness).
    :return: Model's response as a string.
    """
    model_id = "mistral.mistral-7b-instruct-v0:2"
    
    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime")
    
    # Construct the payload
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Convert payload to JSON
    request_body = json.dumps(payload)
    
    attempt = 0
    while attempt < retries:
        try:
            # Invoke Bedrock model
            response = bedrock.invoke_model(
                modelId=model_id,
                body=request_body
            )
            
            # Parse response
            response_body = json.loads(response["body"].read())
            return response_body["outputs"][0]["text"]
        
        except Exception as e:
            if "Throttle" in str(e) or "Rate exceeded" in str(e):
                wait_time = backoff_factor ** attempt
                print(f"Throttle error encountered. Retrying in {wait_time}")
                time.sleep(wait_time)
                attempt += 1
            else:
                print(f"Error invoking Mistral-7B: {e}")
                return None

    print("Max retries reached. Request failed.")
    return None


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

df.to_csv(os.path.join(os.getcwd(),'matched_311_mistral_edibles.csv'),index=False)
