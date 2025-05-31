# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import requests
import base64
import cloudinary
import cloudinary.uploader
from openai import OpenAI
from dotenv import load_dotenv

# === 初始化 ===
app = Flask(__name__)
CORS(app)
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

if __name__ == '__main__':
    app.run(port=3001, debug=True)
