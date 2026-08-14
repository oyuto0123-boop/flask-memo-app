from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/about')
def about():
    return "これはメモアプリです"

@app.route('/goodbye')
def goodbye():
    return "さようなら、世界！"

@app.route('/hello/<name>')
def hello_name(name):
    return f"こんにちは、{name}！"

@app.route("/api/sample", methods=["GET"])
def get_sample():
    return "GETリクエストを受け取りました" 

@app.route("/api/sample", methods=["POST"])
def create_sample():
    return "POSTリクエストを受け取りました"

@app.route("/api/fruits")
def api_fruits():
    fruits = [
        {"id":1,"name":"りんご"},
        {"id":2,"name":"バナナ"},
        {"id":3,"name":"みかん"}
    ]
    return jsonify(fruits)

@app.route("/api/echo", methods=["POST"])
def api_echo():
    data = request.get_json()
    return jsonify({"received": data})

@app.route("/api/create-sample", methods=["POST"])
def create_sample_data():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "name は必須です"}), 400

    return jsonify({"message": f"{data['name']} が作成されました"}), 201


if __name__ == '__main__':
    app.run(debug=True)

