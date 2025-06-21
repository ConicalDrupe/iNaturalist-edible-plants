import boto3
import json
import os

def get_image_list(folder='book_images_v2',ext='.tif'):
    file_list=[]
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=os.environ['AWS_BUCKET'],StartAfter='book_images_v2')
    for page in result:
        if "Contents" in page:
            for key in page[ "Contents" ]:
                keyString = key[ "Key" ]
                if keyString.split('/')[0]==folder and keyString.endswith(ext):
                    file_list.append(keyString)

    return file_list


def extract_json(tif_path):
    tif_name = tif_path.split('/')[1]

    client = boto3.client('textract')

    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': os.environ['AWS_BUCKET'], 'Name': f'{tif_path}'}}
    )


    # Creating json data
    json_data = {}
    json_data['file_name'] = tif_name
    json_data['Blocks'] = {}

    for i,item in enumerate(response['Blocks']):
        if item['BlockType'] == 'LINE' or item['BlockType'] == 'WORD':
            json_data['Blocks'][i] = {}#defaultdict()
            json_data['Blocks'][i]['BlockType'] = item['BlockType']
            json_data['Blocks'][i]['Text'] = item['Text']

    return json_data,tif_name

# s3_tif_file='' # from pagnator object

def save_json_to_s3(json_data,tif_name):
    json_name =  tif_name.split('.')[0] +'.json'

    s3_client = boto3.client('s3')

    s3_client.put_object(Body=bytes(json.dumps(json_data).encode('UTF-8')),
                         Bucket=os.environ['AWS_BUCKET'],
                         Key=f'book_json_v2/{json_name}',
                         ContentType='application/json')
    return True



if __name__ == '__main__':
    tif_list = get_image_list()

    total_len = len(tif_list)

    for i,tif in enumerate(tif_list):
        json_data, tif_name = extract_json(tif)
        code = save_json_to_s3(json_data,tif_name)
        if code:
            print(f'Saved json {tif_name} to S3 [{i}/{total_len}]')
        else:
            print(f'{tif_name} unsuccessfully uploaded')


