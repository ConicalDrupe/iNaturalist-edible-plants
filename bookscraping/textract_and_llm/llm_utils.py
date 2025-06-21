import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json
import time

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
