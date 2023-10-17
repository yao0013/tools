from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 定义一个接口，通过POST请求获取名为'dir'的字段值来查询目录
@app.route('/get_folders', methods=['POST'])
def get_folders():
    try:
        if request.content_type == 'application/json':
            # 处理 JSON 请求
            directory = request.get_json(silent=True).get('dir')
        else:
            # 处理 Form Data 请求
            directory = request.form.get('dir')

        if directory is None:
            return jsonify({'error': 'No valid "dir" parameter provided'})

        # 使用 os 模块列出指定目录下的文件夹
        folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        return jsonify({'folders': folder_list})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='192.168.19.106', port=5000, debug=True)
