from kivymd.app import MDApp

from kivy.lang import Builder

from kivy.properties import BooleanProperty

from kivymd.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.camera import Camera

import numpy as np
import cv2
import pyelsed
import line_tracker

Builder.load_file('mixed_reality_application.kv')

class AndroidCamera(Camera):
    # "There is no built-in API for acquiring the maximum android camera resolution.
    # and in general the kivy.uix.camera is not in a good state on Android."
    # https://stackoverflow.com/questions/62611492/how-to-get-maximum-camera-resolutions-in-kivy-uix-camera
    # Declaring a predetermined camera_resolution.
    camera_resolution = (640, 480)

    _show_tracked = BooleanProperty(False)
    _show_newly_detected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(AndroidCamera, self).__init__(**kwargs)
        
        # self.texture = Texture.create(size=np.flip(self.camera_resolution))
        # self.texture_size = list(self.texture.size)

        self.trackerData = line_tracker.LineFeatureTracker()

    def on_tex(self, camera_core):
        if self._camera._buffer is None:
            return
        
        super().on_tex(camera_core) # Refresh the content of the (internal) texture.
        frame = self.__frame_from_buf()
        self.__frame_to_screen(frame, self._show_tracked, self._show_newly_detected)

    def __frame_from_buf(self):
        w, h = self.resolution
        # frame = np.frombuffer(self.texture.pixels.tostring(), 'uint8').reshape((h + h // 2, w)) # Doesn't work?
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)
        return frame_bgr

    def __frame_to_screen(self, frame, show_tracked:bool = True, show_newly_detected: bool = True):
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        self.trackerData.readImage(frame)
        cur_img = self.trackerData.getCurImg()

        un_lines = cur_img.vecLine
        lineIDs = cur_img.lineID
        successes = cur_img.success

        # Draw newly-detected lines.
        if show_newly_detected:
            for idx, un_line in enumerate(un_lines):
                if successes[idx] != -1:
                    continue # Ignore tracked lines


                start, end = un_line["keyPoint"][0], un_line["keyPoint"][-1]
                start1, end1 = un_line["StartPt"], un_line["EndPt"]

                cv2.line(frame_rgba, start, end, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(frame_rgba, start1, end1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(frame_rgba, str(lineIDs[idx]), un_line["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)

        # Draw tracked lines.
        if show_tracked:
            for idx, un_line in enumerate (un_lines):
                if successes[idx] == -1:
                    continue # Ignore newly-detected lines

                start, end = un_line["keyPoint"][1], un_line["keyPoint"][-1]
                start1, end1 = un_line["StartPt"], un_line["EndPt"]

                cv2.line(frame_rgba, start, end, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.line(frame_rgba, start1, end1, (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(frame_rgba, str(lineIDs[idx]), un_line["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)
        
            
        self.texture.blit_buffer(frame_rgba.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')


        # I haven't managed to get this working, because I cannot debug it.
        # I need to understand what type each image is :/

        # img = cur_img.img
        # # Gradient map
        # gray = img
        # # Compute gradients using Sobel operators
        # grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        # grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        # # Compute the magnitude of the gradient
        # magnitude = np.sqrt(grad_x**2 + grad_y**2)
        # # Normalize the magnitude to the range [0, 255]
        # magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        # # Convert the gradient map to uint8
        # gradient_map = np.uint8(magnitude)
        # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        # gradient_map = cv2.cvtColor(gradient_map, cv2.COLOR_GRAY2RGB)

        # combined = np.hstack((gray, gradient_map))
        # self.texture.blit_buffer(combined.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')



class NegateIconButton(MDIconButton):

    def negate_attribute(self, widget_instance: Widget, attribute_name: str, *args):

        current_boolean_value = getattr(widget_instance, attribute_name)

        if type(current_boolean_value) == bool:
            setattr(widget_instance, attribute_name, not current_boolean_value)
        else:
            raise TypeError(f'Expected {current_boolean_value} to be of type {bool}.'
                            f'{current_boolean_value} is of type {type(current_boolean_value)} instead.')

class MixedRealityApplicationLayout(MDFloatLayout):
    pass

class MyApp(MDApp):
    def build(self):
        return MixedRealityApplicationLayout()

if __name__ == '__main__':
    MyApp().run()
