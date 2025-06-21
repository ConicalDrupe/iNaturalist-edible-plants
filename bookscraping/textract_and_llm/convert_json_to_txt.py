import boto3
import json
import os

def get_json_list(s3_client,folder='book_json_v2',ext='.json'):
    file_list=[]
    paginator = s3_client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=os.environ['AWS_BUCKET'],StartAfter='book_images_v2')
    for page in result:
        if "Contents" in page:
            for key in page[ "Contents" ]:
                keyString = key[ "Key" ]
                if keyString.split('/')[0]==folder and keyString.endswith(ext):
                    file_list.append(keyString)

    return file_list

def load_json_from_s3(s3_client,json_path):

    response = s3_client.get_object( Bucket=os.environ['AWS_BUCKET'],
                         Key=json_path)

    json_data = response['Body'].read().decode('UTF-8')
    data = json.loads(json_data)

    return data


def covert_json_to_txt(json_data,json_name,save_dir):
    with open(os.path.join(save_dir,f'{json_name}.txt'),"w") as txt:
        for block in json_data["Blocks"].values():
            if block["BlockType"]=="LINE":
                txt.write(block["Text"]+"\n")
            if block["BlockType"]=="WORD":
                txt.write(block["Text"]+" ")
    return



if __name__ == '__main__':
    import pandas as pd

    s3_client = boto3.client('s3')
    json_list = get_json_list(s3_client)

    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    save_dir = os.path.join(back_dir,'outputs','txt_files')

    master_ls= []

    json_ls_len = len(json_list)

    for i,json_s3 in enumerate(json_list):
        json_data = load_json_from_s3(s3_client,json_s3)

        txt_name = json_s3.split('/')[1].split('.json')[0]
        
        covert_json_to_txt(json_data,txt_name,save_dir)

        print(f'Converted json {i+1}/{json_ls_len} to txt')

