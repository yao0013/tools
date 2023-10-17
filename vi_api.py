from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/your_api_endpoint', methods=['POST'])
def your_api_endpoint():
    # 从请求中获取字段
    data = request.get_json()
    field1 = data.get('field1')
    field2 = data.get('field2')

    # 检查字段是否存在
    if field1 is None or field2 is None:
        return jsonify({"error": "Both field1 and field2 are required"}), 400

    # 构建要执行的Shell命令
    shell_command = f'your_script.sh {field1} {field2}'

    try:
        # 执行Shell脚本
        result = subprocess.check_output(shell_command, shell=True, universal_newlines=True)
        # 返回Shell脚本的输出
        return jsonify({"output": result.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Script execution failed: {e.stderr}"}), 500


if __name__ == '__main__':
    app.run(host='192.168.19.106', port=5000, debug=True)
