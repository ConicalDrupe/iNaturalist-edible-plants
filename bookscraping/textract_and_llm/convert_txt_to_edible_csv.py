import json
import os

def get_txt_list(txt_dir):
    return [os.path.join(txt_dir,file) for file in os.listdir(txt_dir) if file.endswith('.txt')]

def name_op1(text_file_path):
    name_flag = True
    name_lines=[]
    with open(text_file_path,'r') as file:

        for line in file:
            if 'QUICK' in line or 'DESCRIPTION' in line:
                name_flag=False
            elif name_flag:
                name_lines.append(line)
            elif 'family' in line and name_flag:
                name_flag=False
                name_lines.append(line)
            else:
                continue

        if name_lines:
            print("Found some name")
            return ''.join(name_lines)
        elif name_flag and name_lines:
            print("WARNING: Name search never stopped")
            return ''.join(name_lines)



def food_use_opt1(text_file_path):
    food_use_lines = []
    food_use_flag = False
    with open(text_file_path,'r') as file:
        for line in file:
            if 'COMMENTS' in line or 'WARNING' in line:
                food_use_flag=False
            elif food_use_flag:
                food_use_lines.append(line)
            elif 'FOOD USE' in line or 'USE' in line:
                food_use_flag=True
                food_use_lines.append(line)
            else:
                continue

        # Below checks if list is empty
        if food_use_lines:
            return ''.join(food_use_lines), True
        else:
            return '', False


if __name__ == '__main__':
    import pandas as pd
    one_dir_back = os.path.normpath(os.getcwd() + os.sep + os.pardir)

    txt_dir = os.path.join(one_dir_back,'outputs','txt_files')
    txt_list = get_txt_list(txt_dir)

    master_ls= []

    txt_ls_len = len(txt_list)

    for i,txt_file_path in enumerate(txt_list):
        name_resp = name_op1(txt_file_path)
        food_res, found_flag = food_use_opt1(txt_file_path)

        temp_data = {'source':txt_file_path.split('/')[-1],
                     'name_data':name_resp,
                     'food_data':food_res,
                     'found_edibilty':found_flag}
        master_ls.append(temp_data)

        print(f'Appended txt {i+1}/{txt_ls_len}')

    final_df = pd.DataFrame(master_ls)
    final_df = final_df.sort_values(by='source',ascending=True)

    final_df.to_csv(os.path.join(one_dir_back,'outputs','txt_extract.csv'),index=False)
