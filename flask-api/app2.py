from flask import Flask, request
from flask_restful import Resource, Api
import urllib
import easyocr
import cv2

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return {"about":"Helloword"}

    def post(self):
        some_json = request.get_json()
        return {'you sent ':some_json}, 201


class Multi(Resource):
    def get(self, num):
        return {"result":num*10}


class Ocr(Resource):
    def post(self):
        some_json = request.get_json()

        # download file to local
        urllib.request.urlretrieve(some_json['location'], "ijazah.jpg")

        image_path = 'ijazah.jpg'
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(image_path)

        img = cv2.imread(image_path)
        tag_nama = ''
        obj_result = {"jns":'', "nama":''}

        for idx, detection in enumerate(result):
            if (detection[1].replace(" ", "").upper() == 'IJAZAH') or (tag_nama.lower() == 'nama'):
                text = detection[1]
                obj_result["jns"] = "IJAZAH"
                if obj_result["nama"] == '' and tag_nama.lower() == 'nama':
                    obj_result["nama"] = text

            # clear tag nama
            tag_nama = detection[1]
        return {"result": obj_result}


api.add_resource(Hello, '/')
api.add_resource(Multi, '/multi/<int:num>')
api.add_resource(Ocr, '/ocr')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
