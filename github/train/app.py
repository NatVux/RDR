from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)

# Phục vụ file index.html
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/segment', methods=['POST'])
def segment():
    data = request.json
    print("Received data:", data)
    
    sentence = data.get("sentence", "")
    if not sentence:
        return jsonify({"error": "Câu nhập không được để trống!"}), 400
    
    # Lưu câu vào file tạm
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(sentence)
    
    try:
        # Gọi RDRsegmenter để xử lý phân tách
        process = subprocess.run(
            [sys.executable, "RDRsegmenter.py", "segment", "input.txt", "output.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)
    except subprocess.CalledProcessError as e:
        print("Lỗi khi chạy RDRsegmenter:", e.stderr)
        return jsonify({"error": "Lỗi khi xử lý phân tách."}), 500

    # Đọc kết quả đã phân tách
    if os.path.exists("output.txt"):
        with open("output.txt", "r", encoding="utf-8") as f:
            result = f.read().strip()
    else:
        result = "Không tìm thấy kết quả phân tách."

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
