# from django.shortcuts import render
# from django.http.response import StreamingHttpResponse
# from .camera import VideoCamera


# def index(request):
#     return render(request, 'livestream/home.html')


# # ラップトップのカメラメソッドを呼び出すたびにフレームが取得される
# # 詳細はcamera.pyに記載
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# def video_feed(request):
#     return StreamingHttpResponse(gen(VideoCamera()),
#         content_type='multipart/x-mixed-replace; boundary=frame')



'''
returnではなくジェネレーターのyieldで逐次出力。
Generatorとして働くためにgenとの関数名にしている
Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
multipart/x-mixed-replaceは、HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
（※以下に解説参照あり）
'''

# from django.http import HttpResponse
from django.shortcuts import render
# from .models import *
# from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

def index(request):
    return render(request, 'livestream/home.html')

@gzip.gzip_page
def video_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'livestream/home.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')