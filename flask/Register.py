from flask import Flask, request, jsonify
from flask_cors import CORS
from models import User, SessionLocal

app = Flask(__name__)
CORS(app)  # 允许跨域访问（Vue 会用到）

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
