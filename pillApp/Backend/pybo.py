from flask import Flask, request, jsonify # Flask

app = Flask(__name__)

@app.route('/users')
def users():
	# users 데이터를 Json 형식으로 반환한다
    return {"members": [{ "id" : 1, "name" : "yerin" },
    					{ "id" : 2, "name" : "dalkong" }]}

# Consumer 이미지 POST, GET
@app.route('/image', methods=['GET','POST'])
def consumerImage():
    data = request.json
    return jsonify(data)


# 모델 결과값 불러오기
# @app.route('/result', methods=['GET','POST'])
# def model_result():
#     # if (request.method == "POST"):
#     #     data = request.get_data()
#     #     return "Image Loading"
#     return {"result": [{'id': "pill_1",'name': "세틸란캡슐200mg",'type': "진해거담제",'image': "1.jpg",},
#     					{'id': "pill_2",'name': "뭐 어떤 캡슐",'type': "aa",'image': "2.jpg",},]}
  


if __name__ == "__main__":
    app.run(host = '172.30.1.60', port = 5000, debug = True)
    