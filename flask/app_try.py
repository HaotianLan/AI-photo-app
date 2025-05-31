import os
from google import genai
from google.genai import types
import PIL.Image
from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

_ = load_dotenv(find_dotenv())

if not os.path.exists('static'):
    os.makedirs('static')

app = Flask(__name__)
CORS(app)  # 启用 CORS

@app.route('/upload', methods=['POST'])
def some_logic():
    sys_prompt_text = """这张图片里有什么？"""
    try:
        request.files
    except Exception as e:
        return jsonify({"error": str(e)}), 300
        
    if 'image' not in request.files:
        return jsonify({'message': 'No image file'}), 400
    image_file = request.files['image']
    
    try:
        image = PIL.Image.open(image_file.stream)
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY5"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[sys_prompt_text, image]
        )
        print(response)
        
        answer = response.text
        print(answer)
        
        image_L = PIL.Image.open(image_file.stream).convert('L')
        grayscale_image_path = 'static/grayscale_image.png'
        image_L.save(grayscale_image_path)
        return jsonify({
            'grayscaleImageUrl': f'http://127.0.0.1:5001/{grayscale_image_path}',
            'message': answer
        })
    
    except Exception as e:
        print(f"Error processing the image: {e}")
        return jsonify({'message': f'处理图片失败: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)