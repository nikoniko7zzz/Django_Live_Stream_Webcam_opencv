# from imutils.video import VideoStream
# import imutils
import cv2
# import os, settings
# import urllib.request
# import numpy as np
# from django.conf import settings
import numpy as np
# import pyshine as ps
from PIL import Image, ImageDraw, ImageFont

# 日本語フォントへのパス
FONT_PATH = '/static/livestream/font/NotoSansJP-Regular.otf'

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        text = '日本語テキスト'
        # text = 'test text'
        image = write_text_on_frame(image, text, width, height)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def write_text_on_frame(
    frame: np.ndarray, text: str, width: int, height: int
) -> np.ndarray:
    """入力フレームに指定テキスト書き込み

    Args:
        frame (np.ndarray): フレーム
        text (str): 書き込みテキスト
        width (int): フレーム幅
        height (int): フレーム高

    Returns:
        np.ndarray: テキスト書き込みフレーム
    """
    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)

    # テキストの設定
    font = ImageFont.truetype(font=FONT_PATH, size=20)
    # 白の枠を描画
    draw.rectangle(xy=(0, 0, 200,100), fill=(255, 255, 255))
    # テキストを描画
    draw.text(xy=(10, 10), text=text, fill=(0, 0, 255), font=font)

    return np.array(image)

