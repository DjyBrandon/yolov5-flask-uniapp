import base64
import os
import time

from flask import Flask, jsonify
from flask import redirect
from flask import url_for
from flask import request
from flask_cors import CORS

from config.login import is_existed, exist_user
from config.register import add_user
from detect import run_detect

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if is_existed(username, password):
            user = is_existed(username, password)
            user_id = user[0]
            return {"code": 200, "message": "登录成功", "userId": user_id}
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return {"code": 400, "message": login_massage}
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return {"code": 400, "message": login_massage}


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            return {"code": 400, "message": login_massage}
        else:
            add_user(username, password)
            login_massage = "温馨提示：注册成功"
            return {"code": 200, "message": login_massage}


@app.route('/detect', methods=['POST'])
def detect():
    print(time.time())
    if request.method == 'POST':
        user_id = request.values.get('userId')
        # 获取上传的文件
        files = request.files.getlist('file')
        # 返回图片流
        encoded_images = []

        user_path = os.path.join('origin', user_id)
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        else:
            pass

        # 保存文件到一个位置
        for file in files:
            filename = os.path.splitext(file.filename)[0]

            origin = os.path.join('origin', user_id, file.filename)
            file.save(origin)
            # 调用 YOLOv5 检测
            results = run_detect(origin, filename)
            # 处理结果，将其返回给前端
            with open(origin, 'rb') as f:
                ori = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

            with open(results, 'rb') as f:
                det = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

            encoded_images.append({'ori': ori, 'det': det})

        return jsonify(encoded_images)


@app.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('userId')
    print(user_id)
    folder_path = "detect"
    image_files = []
    for file_name in os.listdir(folder_path):
        for file in os.listdir(folder_path+"/"+file_name):
            if file.endswith(".jpg"):
                # 处理结果，将其返回给前端
                with open(folder_path+"/"+file_name+"/"+file, 'rb') as f:
                    det = base64.b64encode(f.read())
                    detect_img = str(det, encoding="utf-8")
                image_files.append(detect_img)

    return image_files


if __name__ == "__main__":
    app.run()
