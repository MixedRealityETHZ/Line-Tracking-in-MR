from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import cv2
import pyelsed

Builder.load_file("myapplayout.kv")

class AndroidCamera(Camera):
    camera_resolution = (640, 480)

    def __init__(self, **kwargs):
        super(AndroidCamera, self).__init__(**kwargs)
        
        self.texture = Texture.create(size=np.flip(self.camera_resolution))
        self.texture_size = list(self.texture.size)

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return None
        frame = self.frame_from_buf()
        self.frame_to_screen(frame)
        super(AndroidCamera, self).on_tex(*l)

    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)
        return frame_bgr

    def frame_to_screen(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGBA2GRAY)
        segments, scores = pyelsed.detect(gray)

        for s in segments.astype(np.int32):
            cv2.line(frame_rgb, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 1, cv2.LINE_AA)
            
        self.texture.blit_buffer(frame_rgb.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()