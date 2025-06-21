
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


def name_op1(json_data):
    name_lines = []
    name_flag=True

    for item in json_data['Blocks'].values():
        if 'QUICK' in item['Text'] or 'DESCRIPTION' in item['Text']:
            name_flag=False
        elif name_flag:
            name_lines.append(item['Text'])
        elif 'family' in item['Text'] and name_flag:
            name_flag=False
            name_lines.append(item['Text'])
        else:
            continue

    if name_lines:
        print("Found some name")
        return name_lines
    elif name_flag and name_lines:
        print("WARNING: Name search never stopped")
        return name_lines



def food_use_opt1(json_data):
    food_use_lines = []
    food_use_flag = False
    for item in json_data['Blocks'].values(): # is this ordered?
        if 'COMMENTS' in item['Text'] or 'WARNING' in item['Text']:
            food_use_flag=False
        elif food_use_flag:
            food_use_lines.append(item['Text'])
        elif 'FOOD USE' in item['Text']:
            food_use_flag=True
            food_use_lines.append(item['Text'])
        else:
            continue

    # Below checks if list is empty
    if food_use_lines:
        return ''.join(food_use_lines), True
    else:
        return '', False


if __name__ == '__main__':
    import pandas as pd

    s3_client = boto3.client('s3')
    json_list = get_json_list(s3_client)

    master_ls= []

    json_ls_len = len(json_list)

    for i,json_s3 in enumerate(json_list):
        data = load_json_from_s3(s3_client,json_s3)
        name_resp = name_op1(data)
        food_res, found_flag = food_use_opt1(data)

        temp_data = {'source':json_s3.split('/')[1],
                     'name_data':name_resp,
                     'food_data':food_res,
                     'found_edibilty':found_flag}
        master_ls.append(temp_data)

        print(f'Appended json {i+1}/{json_ls_len}')

    final_df = pd.DataFrame(master_ls)
    one_dir_back = os.path.normpath(os.getcwd() + os.sep + os.pardir)

    final_df.to_csv(os.path.join(one_dir_back,'outputs','book_extract.csv'),index=False)

    # Save final df to s3
    # s3_client.put_object(Bucket=os.environ['AWS_BUCKET'],Key='csvs/book_name_and_edibility_extract.csv')
