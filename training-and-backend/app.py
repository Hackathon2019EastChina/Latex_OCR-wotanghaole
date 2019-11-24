from flask import request, Flask, send_file
import time
import os
import cv2
import pickle
import numpy as np
import evaluate
import os
import shutil
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index_page():
    return 'Hello, World!'

@app.route("/upload_image", methods=['POST'])
def upload_image():
    startTime = time.time()
    received_file = request.files['input_image']
    

    if received_file:

        
        # im = Image.open(received_file)
        # im.resize((256,256),Image.ANTIALIAS)

        received_dirPath = './data/test/2015'
        imageFileName = received_file.filename
        filepath = os.path.join(received_dirPath,imageFileName)

        if os.path.isfile(filepath):
            os.remove(filepath)
            print(str(filepath) + "removed!")
        
        received_file.save(filepath)

        size = (256,256)
        pri_image = Image.open(filepath)
        pri_image.resize(size, Image.ANTIALIAS).save(filepath)
        
    

        print('image file saved to %s' % filepath)
        usedTime = time.time() - startTime
        print('接收图片并保存，总共耗时%.2f秒' % usedTime)
        startTime = time.time()
        predict_latex = evaluate.main()


        usedTime = time.time() - startTime
        print('完成对接收图片的分类预测，总共耗时%.2f秒' % usedTime)
        print(predict_latex)
        return predict_latex
    else:
        return 'failed'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)