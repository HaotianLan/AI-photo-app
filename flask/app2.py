import os
import io
import time
import requests
import json
import folium
from datetime import datetime, timedelta
import base64
from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
from method import get_image_label#从同一目录下的method.py调取函数get_image_label
from PIL import Image
from ScanImage2 import ImageLabelRetriever
import jwt
from functools import wraps
from models import User, SessionLocal
from method import get_image_label
import uuid
import cloudinary
import cloudinary.uploader
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__, static_folder='xhs_school')
CORS(app)

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
        database_path='image_database.pt',
        label_json_path='/Users/lanhaotian/Desktop/python/OpenAI/flask/xhs_school_change2.json',
        device='mps',
        api_key_env_var='GOOGLE_API_KEY6',
        image_base_dir='/Users/lanhaotian/Desktop/python/OpenAI/flask'
    )

    results = retriever.retrieve_similar_images('uploaded_scan_image.jpg')
    #print(results[0])
    base_url = 'http://localhost:5001/'
    output = []

    for item in results:
        img_rel = os.path.relpath(item['img_path'], start='/Users/lanhaotian/Desktop/python/OpenAI/flask')
        line_rel = item['line_path']  # 已是相对路径

        output.append({
            "Scanned_image": base_url + img_rel,
            "GuideLine_image": base_url + line_rel,
            "prompt": item['prompt']
        })
    #print(output[0])

    return jsonify(output)


@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('xhs_school', filename)

@app.route('/xhs_school_output/<path:filename>')
def serve_output_image(filename):
    return send_from_directory('xhs_school_output', filename)

#####定位
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
    
    
#####AI talk
load_dotenv()

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# === 配置豆包和cloudinary ===
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

# === 上传图片到 Cloudinary 并返回URL ===
def upload_image_to_cloudinary(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        return upload_result['secure_url']
    except Exception as e:
        raise Exception(f"上传到Cloudinary失败: {str(e)}")

# === 文本对话接口 ===
@app.route('/chat/text', methods=['POST'])
def chat_text():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    prompt = f"""
你是一个专业摄影顾问，善于解答用户在拍摄地点、风格选择、器材、构图等方面的各种摄影问题。请根据用户输入，给予简洁清晰的专业建议。

用户提问：{user_message}
"""

    try:
        response = client.chat.completions.create(
            model="doubao-1.5-vision-pro-250328",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("文本接口出错：", e)
        return jsonify({"error": str(e)}), 500

# === 图片+文字分析接口 ===
@app.route('/chat/image', methods=['POST'])
def image_analysis():
    if 'file' not in request.files:
        return jsonify({"error": "Missing image file"}), 400
    file = request.files['file']
    user_text = request.form.get("text", "请点评这张照片。")

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        image_url = upload_image_to_cloudinary(filepath)

        os.remove(filepath)  # 删除本地文件

        # 调用豆包API
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": f"""
你是一个摄影导师，请从构图、光线、姿势、背景等方面评价用户上传的这张照片，同时回答用户提出的问题：{user_text}
"""}
            ]
        }]

        response = client.chat.completions.create(
            model="doubao-1.5-vision-pro-250328",
            messages=messages
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        # 出错时也删除临时文件
        if os.path.exists(filepath):
            os.remove(filepath)
        print("图片接口出错：", e)
        return jsonify({"error": str(e)}), 500
    
#####login
# 秘密密钥，用于加密JWT
SECRET_KEY = "your_secret_key"

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    username = data.get('username')
    password = data.get('password')
    print(f"尝试登录用户: {username}")

    db = SessionLocal()

    # 查询数据库中是否存在该用户
    user = db.query(User).filter_by(username=username).first()

    if not user:
        db.close()
        return jsonify({'message': '用户不存在'}), 401

    if user.password != password:
        db.close()
        return jsonify({'message': '密码错误'}), 401

    # 登录成功，生成 JWT
    token = jwt.encode(
        {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm='HS256'
    )

    db.close()
    return jsonify({'token': token})



# 验证 JWT 的装饰器
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # 获取请求头中的 JWT
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # 获取 Bearer 后的部分
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # 解码并验证 JWT
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']  # 你可以获取到存储在 JWT 中的任何信息
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function


# 图片推荐的 API
#@app.route('/recommend', methods=['POST'])
#@token_required  # 使用装饰器来保护这个路由
#def recommend(current_user):
#    data = request.get_json()
#    search_query = data.get('search_query', '')
#    
#    # 假设我们通过某种算法得到推荐图片列表
#    recommended_images = os.listdir(STATIC_FOLDER)
#    
#    # 返回完整的图片 URL
#    base_url = 'http://localhost:5001/static/'
#    recommended_image_urls = [base_url + image for image in recommended_images]
#    print('成功返回')
#    return jsonify({'recommended_images': recommended_image_urls})

    
@app.route('/verify', methods=['GET'])
def verify():
    # 从请求头中获取Authorization字段
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({'message': 'Missing token'}), 401

    # 提取Bearer token部分
    token = auth_header.split(" ")[1]  # 格式为: "Bearer <token>"

    try:
        # 解码JWT
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # 如果成功，返回解码后的内容
        return jsonify({'message': 'JWT is valid', 'user': decoded_token['username']})
    except jwt.ExpiredSignatureError:
        # 如果JWT过期
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        # 如果JWT无效
        return jsonify({'message': 'Invalid token'}), 401
    
#####注册
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    db = SessionLocal()

    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return jsonify({"success": False, "message": "用户名已存在"})

    # 插入新用户
    new_user = User(username=username, password=password, email=email)
    db.add(new_user)
    db.commit()
    db.close()

    return jsonify({"success": True, "message": "注册成功"})
####search
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
    json_name = 'Image_label_change.json'
    json_name = 'xhs_school.json'
    recommended_images = get_image_label(selected_tags,json_name)
    recommended_images = [image.split('/')[1] for image in recommended_images]
    base_url = 'http://localhost:5001/static/'
    recommended_image_urls = [base_url + image for image in recommended_images]
    # 返回推荐的图片 URL
    #print({"recommended_images": recommended_image_urls})
    return jsonify({"recommended_images": recommended_image_urls})



if __name__ == '__main__':
    app.run(port=5001, debug=True)