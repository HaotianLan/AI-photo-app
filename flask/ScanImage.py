import os
import json
import torch
import open_clip
import numpy as np
from PIL import Image
from dotenv import load_dotenv, find_dotenv
import torchvision.transforms as transforms
from google import genai

class ImageLabelRetriever:
    def __init__(self,
                 database_path='image_database.pt',
                 label_json_path='image_labels.json',
                 device='mps',
                 api_key_env_var='GOOGLE_API_KEY6',
                 image_base_dir='/Users/lanhaotian/Desktop/python/OpenAI/flask/Image'):

        load_dotenv(find_dotenv())
        self.device = device
        self.database_path = database_path
        self.label_json_path = label_json_path
        self.image_base_dir = image_base_dir
        self.api_key = os.getenv(api_key_env_var)

        self.label_weight = {
            '季节主题': 0.1, '节日主题': 0.2, '特殊活动': 0.2,
            '场景': 0.5, '时间': 0.1, '天气': 0.1
        }

        # 加载模型和预处理
        self.model, self.preprocess, _ = open_clip.create_model_and_transforms(
            'ViT-B-32', pretrained='laion2b_s34b_b79k', device=device
        )

        # 加载特征数据库
        self.database = torch.load(self.database_path)
        self.database_features = self.database['features']  # [N, D]
        self.database_paths = self.database['paths']

        # Google Gemini 客户端初始化
        self.client = genai.Client(api_key=self.api_key)

        # 标签提示语
        self.sys_prompt_text = """
你是一个为给图片进行分类打标签的专家，可以根据图片内容，为图片分类并打标签。
下面的<LABEL-INFO></LABEL-INFO>内是标签的具体信息，你需要根据这些标签给图片分类。
标签分为一级标签和二级标签，回答的文本内容格式为一级标签:二级标签，二级标签。
一个一级标签可以对应多个二级标签
场景必须给出
节日主题和特殊活动如果看不出来则不需要给。
季节主题如果不明显则通过人物的穿着冷暖来判断，如果无法分辨是春季还是秋季请都列出。

<LABEL-INFO>
| 一级标签 | 二级标签|
| --- | --- |
| 季节主题 | 春季/夏季/秋季/冬季 |
| 节日主题 | 春节/万圣节/圣诞节/情人节/端午节/中秋节 |
| 特殊活动 | 婚礼/毕业/生日/旅行 |
| 场景 | 家庭/影棚/咖啡馆/图书馆/精品店/教室/CBD/历史街区/天台/地铁站/桥梁/街道/中式园林/公园草地/湖泊/路牌/动物园/迪士尼/漫展/自然/操场 |
| 时间 | 清晨/正午/黄昏/夜晚/黄金时刻 |
| 天气 | 晴天/雾霾/阴天/绵绵小雨/大雨/飘雪/大雪/极光 |
</LABEL-INFO>
"""

    def _get_labels_from_image(self, image_path):
        image = Image.open(image_path)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[self.sys_prompt_text, image]
        )
        return self._parse_labels(response.text)

    def _parse_labels(self, answer):
        label = {'季节主题': None, '节日主题': None, '特殊活动': None, '场景': None, '时间': None, '天气': None}
        lines = answer.strip().split('\n')
        for line in lines:
            line = line.replace(' ', '').replace('*', '').replace('-', '')
            if ':' in line:
                key, val = line.split(':', 1)
                if key in label:
                    if ',' in val:
                        label[key] = val.split(',')
                    elif '，' in val:
                        label[key] = val.split('，')
                    elif '/' in val:
                        label[key] = val.split('/')
                    else:
                        label[key] = [val]
        return label

    def _compute_similarity(self, query_image_path):
        image = Image.open(query_image_path).convert("RGB")
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            features = self.model.encode_image(image_input)
            features = features / features.norm(dim=-1, keepdim=True)
        similarities = (self.database_features @ features.cpu().T).squeeze(1)
        return {path: sim.item() for path, sim in zip(self.database_paths, similarities)}

    def retrieve_similar_images(self, query_image_path):
        label = self._get_labels_from_image(query_image_path)
        similarities = self._compute_similarity(query_image_path)

        with open(self.label_json_path, 'r') as f:
            label_db = json.load(f)

        scored_images = []
        for entry in label_db:
            score = 0
            img = entry['img']
            label_dic = entry['label']

            for key in label:
                if label[key] is not None and label_dic.get(key) is not None:
                    # 有交集即可
                    if set(label[key]) & set(label_dic[key]):
                        score += self.label_weight[key]

            img_path_full = os.path.join(self.image_base_dir, img)
            score += similarities.get(img_path_full, 0)
            scored_images.append([img, score])

        scored_images.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored_images]