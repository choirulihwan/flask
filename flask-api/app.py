from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        some_json = request.get_json()
        return jsonify({'you sent ':some_json}), 201
    else:
        return jsonify({"about":"Helloword"})


@app.route('/multi/<int:num>', methods=['GET'])
def get_multiply(num):
    return jsonify({"result":num*10})


if __name__ == '__main__':
    app.run(debug=True, port=5000)