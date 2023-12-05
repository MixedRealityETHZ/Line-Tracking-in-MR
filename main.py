from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import cv2
import pyelsed
import line_tracker

Builder.load_file("myapplayout.kv")
# VIS_TRACK=False

class AndroidCamera(Camera):
    camera_resolution = (640, 480)

    def __init__(self, **kwargs):
        super(AndroidCamera, self).__init__(**kwargs)
        
        self.texture = Texture.create(size=np.flip(self.camera_resolution))
        self.texture_size = list(self.texture.size)

        self.trackerData = line_tracker.LineFeatureTracker()

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
        
        # gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGBA2GRAY)
        # segments, scores = pyelsed.detect(gray)
        # for s in segments.astype(np.int32):
        #     cv2.line(frame_rgb, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 1, cv2.LINE_AA)
        self.trackerData.readImage(frame)
        cur_img = self.trackerData.getCurImg()
        # img = cur_img.img
        # tmp_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        un_lines = cur_img.vecLine
        lineIDs = cur_img.lineID
        successes = cur_img.success

        for j in range(len(un_lines)):
            if successes[j] != -1:
                continue
            
            start = un_lines[j]["keyPoint"][1]
            end = un_lines[j]["keyPoint"][-1]
            start1 = un_lines[j]["StartPt"]
            end1 = un_lines[j]["EndPt"]

            cv2.line(frame_rgb, start, end, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.line(frame_rgb, start1, end1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame_rgb, str(lineIDs[j]), un_lines[j]["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)
        
        un_lines = cur_img.vecLine
        for m in range(len(un_lines)):
            if successes[m] == -1:
                break

            start = un_lines[m]["keyPoint"][1]
            end = un_lines[m]["keyPoint"][-1]
            start1 = un_lines[m]["StartPt"]
            end1 = un_lines[m]["EndPt"]

            cv2.line(frame_rgb, start, end, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.line(frame_rgb, start1, end1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame_rgb, str(lineIDs[m]), un_lines[m]["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)
        
        # if VIS_TRACK:
        #     detect_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        #     lineRec = cur_img.lineRec

        #     for m in range(len(lineRec)):
        #         lines = lineRec[m]
                
        #         if len(lines) > 20:
        #             lines = lines[-20:]
                
        #         for j in range(len(lines)):
        #             start = lines[j]["start"]
        #             end = lines[j]["end"]

        #             if j == len(lines) - 1:
        #                 cv2.line(detect_img, start, end, (0, 255, 0), 2, cv2.LINE_AA)
        #             else:
        #                 cv2.line(detect_img, start, end, (0, 0, 55 + 10 * j), 1, cv2.LINE_AA)
            
        self.texture.blit_buffer(frame_rgb.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()