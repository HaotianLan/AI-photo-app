import json

def get_image_label(label,json_name):
    with open(json_name,"r") as f:
        load_prompt = json.load(f)
    lst_image = []
    for item in label:
        #print(item)
        for j in range(len(load_prompt)):
            img = load_prompt[j]['img']
            label_dic = load_prompt[j]['label']
            if item in label_dic:
                if label_dic[item] == True:
                    lst_image.append(img)
                    #print(label_dic[item])
    return lst_image


