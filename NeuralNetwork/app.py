from flask_cors import CORS
import os
from flask import Flask, jsonify, request
from process import mainProcess

app = Flask(__name__)
CORS(app)

@app.route("/execute", methods=['POST','GET'])
def execute():
    json_data = request.json
    #手寫辨識
    result_array = mainProcess()
    print(result_array)

    return jsonify({'trueNum': int(result_array[1]), 'predictNum': int(result_array[0]), 'index': int(result_array[2])})

#刪除圖片
@app.route("/deleteImage", methods=['POST','GET'])
def deleteImage():
    json_data = request.json
    index = json_data["index"]
    image_path = '/app/img/num_' + index + '.png'
    if os.path.isfile(image_path):
        os.remove(image_path)

    return index

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)