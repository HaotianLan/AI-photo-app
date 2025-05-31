import os
import io
import time
import requests
import json
import folium
from datetime import datetime
import base64
from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
from method import get_image_label#从同一目录下的method.py调取函数get_image_label
from PIL import Image
from ScanImage import ImageLabelRetriever


#前置操作，static_folder='Image'将Image这一目录设置为static_folder方便提取图片
app = Flask(__name__, static_folder='xhs_school')
CORS(app)
#IMAGE_ROOT = os.path.abspath('/Users/lanhaotian/Desktop/python/OpenAI/flask')

#/recommend和POST要与前端await的代码一致
@app.route('/recommend', methods=['POST'])
def recommend_images():
    # 先尝试是否能够连接成功
    try:
        request.get_json()
    except Exception as e:
        return jsonify({"error": str(e)}), 300
    #获取请求中的参数
    params = request.get_json()
    #const params = {
    #  q: searchQuery.value.trim(),
    #  selectedTags: selectedTags.value.join(',')
    #}
    #这里前端的参数为params，它定义了两部分为别为q和selectedTags对应params.get('q', '')和params.get('selectedTags', '').split(',')
    #print出来两个量来检查
    query = params.get('q', '')
    print(query)
    selected_tags = params.get('selectedTags', '').split(',')
    print(selected_tags)
    #执行搜索功能，调用写好的函数get_image_label(method.py里)
    json_name = 'xhs_school.json'
    recommended_images = get_image_label(selected_tags,json_name)
    recommended_images = [image.split('/')[1] for image in recommended_images]
    #print('isexit:{}'.format(os.path.exists(recommended_images[0])))
    base_url = 'http://localhost:5001/static/'
    recommended_image_urls = [base_url + image for image in recommended_images]
    print('recommended_image_urls:{}'.format(recommended_image_urls[0]))
    # 返回推荐的图片 URL
    #print({"recommended_images": recommended_image_urls})
    return jsonify({"recommended_images": recommended_image_urls})


@app.route('/ScanImage', methods=['POST'])
def scan_images():
    try:
        request.json.get('image')
    except Exception as e:
        return jsonify({"error": str(e)}), 300
    data = request.json.get('image')
    image_data = base64.b64decode(data)
    image = Image.open(io.BytesIO(image_data))
    
    image.save('uploaded_scan_image.jpg')
    retriever = ImageLabelRetriever(
        database_path='image_database.pt',              # 图像特征库
        label_json_path='/Users/lanhaotian/Desktop/python/OpenAI/flask/xhs_school.json',# 图像标签信息
        device='mps',                                    # 可用 'cuda', 'cpu', 'mps'
        api_key_env_var='GOOGLE_API_KEY6',              # .env 中的 key 名
        image_base_dir='/Users/lanhaotian/Desktop/python/OpenAI/flask'  # 存图目录
    )
    
    results = retriever.retrieve_similar_images('uploaded_scan_image.jpg')
    results = [image.split('/')[1] for image in results]
    print(results[0])

    base_url = 'http://localhost:5001/static/'
    Scanned_image_urls = [base_url + image for image in results]
    print(Scanned_image_urls[0])
    GuideLine_image_urls = [base_url + image for image in results]

    return jsonify({"Scanned_images": Scanned_image_urls, 'GuideLine_images':GuideLine_image_urls})

#将图片上传到http://localhost:5001/static/
@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory('xhs_school', filename)

#将图片上传到http://localhost:5001/static/
#@app.route('/fuzhuxian/<filename>')
#def serve_image(filename):
#    return send_from_directory('xhs_school_output', filename)


# 配置常量
AMAP_API_KEY = os.getenv('AMAP_API_KEY', '415742a24b233b7c52f8a380df7118b2')
POI_FOLDER = r"/Users/lanhaotian/Desktop/python/OpenAI/flask/仙林校区打卡点"
OUTPUT_DIR = r"/Users/lanhaotian/Desktop/python/OpenAI/flask"
CACHE_ENABLED = True
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}



class DistanceCache:
    """步行距离缓存"""
    def __init__(self):
        self.cache = {}
    
    def get_key(self, origin, destination):
        return f"{origin}|{destination}"
    
    def get(self, origin, destination):
        return self.cache.get(self.get_key(origin, destination))
    
    def set(self, origin, destination, distance):
        self.cache[self.get_key(origin, destination)] = distance

distance_cache = DistanceCache() if CACHE_ENABLED else None

# 静态文件路由
@app.route('/photos/<path:filename>')
def serve_photo(filename):
    """提供POI图片"""
    if not is_safe_filename(filename):
        abort(403)
    return send_from_directory(POI_FOLDER, filename)

@app.route('/maps/<path:filename>')
def serve_map(filename):
    """提供生成的地图文件"""
    return send_from_directory(OUTPUT_DIR, filename)

def is_safe_filename(filename):
    """检查文件名安全性"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_poi_list(folder_path):
    """从图片文件名提取POI信息（返回带URL的列表）"""
    poi_list = []
    
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"打卡点目录不存在: {folder_path}")
    
    for filename in os.listdir(folder_path):
        if not is_safe_filename(filename):
            continue
        
        try:
            name_part = os.path.splitext(filename)[0]
            name, coords = name_part.rsplit('-', 1)
            longitude, latitude = map(float, coords.split(','))
        except (ValueError, IndexError) as e:
            print(f"跳过无效文件名: {filename} ({str(e)})")
            continue
        
        poi_list.append({
            'name': name.strip(),
            'location': f"{longitude},{latitude}",
            'photo_url': url_for('serve_photo', filename=filename, _external=True)
        })
    
    return poi_list

def get_walking_distance(api_key, origin, destination):
    """获取步行距离（带缓存）"""
    if CACHE_ENABLED:
        cached = distance_cache.get(origin, destination)
        if cached is not None:
            return cached
    
    url = "https://restapi.amap.com/v3/direction/walking"
    params = {
        "key": api_key,
        "origin": origin,
        "destination": destination
    }
    
    for attempt in range(3):
        try:
            if attempt > 0:
                time.sleep(1.5 * (attempt + 1))
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "1":
                error_code = data.get("infocode", "未知")
                print(f"API错误: {data.get('info')} (错误码: {error_code})")
                return None
            
            distance = int(data["route"]["paths"][0]["distance"])
            if CACHE_ENABLED:
                distance_cache.set(origin, destination, distance)
            return distance
            
        except (requests.RequestException, KeyError) as e:
            print(f"请求失败: {str(e)}")
    
    return None

def recommend_pois(api_key, current_loc, folder_path):
    """主推荐函数"""
    if not all(map(lambda x: x.strip(), current_loc.split(','))):
        raise ValueError("无效的坐标格式")
    
    try:
        all_pois = get_poi_list(folder_path)
    except Exception as e:
        print(f"获取POI列表失败: {str(e)}")
        return []
    
    recommended = []
    for poi in all_pois:
        distance = get_walking_distance(api_key, current_loc, poi["location"])
        if distance and distance < 1000:
            poi["distance"] = distance
            recommended.append(poi)
    
    return sorted(recommended, key=lambda x: x["distance"])

def show_on_map(recommendations, center_loc, output_dir):
    """生成可视化地图并返回访问URL"""
    try:
        lat, lng = map(float, center_loc.split(',')[::-1])
    except ValueError:
        raise ValueError("中心坐标格式错误")
    
    m = folium.Map(
        location=[lat, lng],
        zoom_start=15,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='高德地图',
        crs='EPSG3857'
    )
    
    for poi in recommendations:
        try:
            lng, lat = map(float, poi["location"].split(','))
            popup_content = f"""
                <b>{poi['name']}</b><br>
                距离: {poi.get('distance', '未知')}米<br>
                <img src="{poi['photo_url']}" width="200">
            """
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(popup_content, max_width=250),
                icon=folium.Icon(color='red')
            ).add_to(m)
        except Exception as e:
            print(f"标记点添加失败: {str(e)}")
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"campus_map_{timestamp}.html"
    output_path = os.path.join(output_dir, filename)
    
    try:
        m.save(output_path)
        return url_for('serve_map', filename=filename, _external=True)
    except Exception as e:
        print(f"地图保存失败: {str(e)}")
        return None

@app.route('/api/nearby_pois', methods=['GET'])
def get_nearby_pois():
    """API端点：获取附近打卡点"""
    current_loc = request.args.get('location')
    if not current_loc:
        return jsonify({'error': '缺少location参数'}), 400
    
    try:
        recommendations = recommend_pois(AMAP_API_KEY, current_loc, POI_FOLDER)
        map_url = show_on_map(recommendations, current_loc, OUTPUT_DIR) if recommendations else None
        print({
            'pois': [{
                'name': p['name'],
                'location': p['location'],
                'photo_url': p['photo_url'],
                'distance': p.get('distance')
            } for p in recommendations],
            'map_url': map_url
        })
        return jsonify({
            'pois': [{
                'name': p['name'],
                'location': p['location'],
                'photo_url': p['photo_url'],
                'distance': p.get('distance')
            } for p in recommendations],
            'map_url': map_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    app.run(port=5001,debug=True)


