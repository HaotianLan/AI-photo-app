import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from method import get_image_label#从同一目录下的method.py调取函数get_image_label
from SearchImage import ImageLabelRetriever

#前置操作，static_folder='Image'将Image这一目录设置为static_folder方便提取图片
app = Flask(__name__, static_folder='xhs_school')
CORS(app)
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
    json_name = 'Image_label_change.json'
    recommended_images = get_image_label(selected_tags,json_name)
    base_url = 'http://localhost:5001/static/'
    recommended_image_urls = [base_url + image for image in recommended_images]
    # 返回推荐的图片 URL
    #print({"recommended_images": recommended_image_urls})
    return jsonify({"recommended_images": recommended_image_urls})

@app.route('/ScanImage', methods=['POST'])
def scan_image():
    try:
        data = request.json.get('image')
        
        # Decode the base64 string into image bytes
        image_data = base64.b64decode(data)
        
        # Convert image bytes to an image using PIL
        image = Image.open(io.BytesIO(image_data))
        
        # You can now perform any processing on the image
        # For example, save it:
        image.save('uploaded_image.jpg')

        # Return a success response
        return jsonify({"message": "Image uploaded and processed successfully."}), 200
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 400
def scan_images():
    try:
        request.json.get('image')
    except Exception as e:
        return jsonify({"error": str(e)}), 300
    data = request.json.get('image')
    image_data = base64.b64decode(data)
    image = Image.open(io.BytesIO(image_data))
    
    query = params.get('q', '')
    print(query)
    selected_tags = params.get('selectedTags', '').split(',')
    print(selected_tags)
    #执行搜索功能，调用写好的函数get_image_label(method.py里)
    json_name = 'Image_label_change.json'
    recommended_images = get_image_label(selected_tags,json_name)
    base_url = 'http://localhost:5001/static/'
    recommended_image_urls = [base_url + image for image in recommended_images]
    #返回推荐的图片 URL
    #print({"recommended_images": recommended_image_urls})
    return jsonify({"recommended_images": recommended_image_urls})

#将图片上传到http://localhost:5001/static/
@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory('xhs_school', filename)

if __name__ == '__main__':
    app.run(port=5001,debug=True)


