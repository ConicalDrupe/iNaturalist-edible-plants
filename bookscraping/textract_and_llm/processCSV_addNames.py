
import os
import boto3
import json
import time
import pandas as pd
from botocore.exceptions import BotoCoreError, ClientError

df = pd.read_csv(os.path.join(os.getcwd(),'book_extract.csv'))

matched = df[df['found_edibilty']==True].reset_index(drop=True)

def call_mistral_7b(prompt,  max_tokens=512, temperature=0.7,retries=5, backoff_factor=2):
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
