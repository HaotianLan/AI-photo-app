from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS
from functools import wraps
import os
from models import User, SessionLocal

app = Flask(__name__)
CORS(app)  # 启用 CORS

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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm='HS256'
    )

    db.close()
    return jsonify({'token': token})

# 登录接口
@app.route('/register', methods=['POST'])
def register():
    # 获取前端传递的数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    print(username,password,email)

    # 检查用户名是否已存在
    #user = User.query.filter_by(username=username).first()
    #if user:
    #    return jsonify({"success": False, "message": "账户名已存在"}), 400
    if username == "都不许去星铁演唱会":
        return jsonify({"success": False, "message": "账户名已存在"}), 400

    # 检查邮箱是否已存在
    #existing_email = User.query.filter_by(email=email).first()
    #if existing_email:
    #    return jsonify({"success": False, "message": "邮箱已被注册"}), 400

    # 创建新用户
    #new_user = User(username=username, password=password, email=email)

    # 保存到数据库
    #db.session.add(new_user)
    #db.session.commit()

    # 注册成功，返回成功响应
    return jsonify({"success": True, "message": "注册成功"}), 201

STATIC_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = STATIC_FOLDER


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
@app.route('/recommend', methods=['POST'])
@token_required  # 使用装饰器来保护这个路由
def recommend(current_user):
    data = request.get_json()
    search_query = data.get('search_query', '')
    
    # 假设我们通过某种算法得到推荐图片列表
    recommended_images = os.listdir(STATIC_FOLDER)
    
    # 返回完整的图片 URL
    base_url = 'http://localhost:5001/static/'
    recommended_image_urls = [base_url + image for image in recommended_images]
    print('成功返回')
    return jsonify({'recommended_images': recommended_image_urls})

    
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

if __name__ == '__main__':
    app.run(port=5001, debug=True)