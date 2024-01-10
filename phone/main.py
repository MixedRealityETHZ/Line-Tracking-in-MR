# from kivy.config import Config
# Config.set('graphics', 'maxfps', '30')

from kivy.clock import Clock
from kivymd.app import MDApp

from kivy.lang import Builder

from kivy.properties import BooleanProperty, NumericProperty

from kivymd.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.camera import Camera

import numpy as np
import cv2
import pyelsed
import line_tracker

Builder.load_file('mixed_reality_application.kv')

colors = [
    # (0, 0, 255),
    (21, 0, 234),
    (42, 0, 213),
    (64, 0, 191),
    (85, 0, 170),
    (106, 0, 149),
    (128, 0, 128),
    (149, 0, 106),
    (170, 0, 85),
    (191, 0, 64),
    (213, 0, 42),
    (234, 0, 21),
    (255, 0, 0),
    (234, 21, 0),
    (213, 42, 0),
    (191, 64, 0),
    (170, 85, 0),
    (149, 106, 0),
    (128, 128, 0),
    (106, 149, 0)
]

class AndroidCamera(Camera):
    # "There is no built-in API for acquiring the maximum android camera resolution.
    # and in general the kivy.uix.camera is not in a good state on Android."
    # https://stackoverflow.com/questions/62611492/how-to-get-maximum-camera-resolutions-in-kivy-uix-camera
    # Declaring a predetermined camera_resolution.
    camera_resolution = (640, 480)

    _show_tracked = BooleanProperty(False)
    _show_newly_detected = BooleanProperty(False)
    _is_ELSED_used = BooleanProperty(False)
    _is_detector_only = BooleanProperty(False)
    _nr_afterimage_lines = NumericProperty(0); _nr_afterimage_min, _nr_afterimage_max = 0, 20 
    
    # Defining the `nr_afterimage_lines` and its setter to make certain
    # that the attribute does not exceed the bounds when called/manipulated.
    @property
    def nr_afterimage_lines(self):
        return self._nr_afterimage_lines
    
    @nr_afterimage_lines.setter
    def nr_afterimage_lines(self, val):
        if self._nr_afterimage_min <= val <= self._nr_afterimage_max:
            self._nr_afterimage_lines = val


        

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

        if self._is_detector_only:
            if self._is_ELSED_used:
                gray = cv2.cvtColor(frame_rgba, cv2.COLOR_RGBA2GRAY)
                segments, scores = pyelsed.detect(gray)
                for s in segments.astype(np.int32):
                    cv2.line(frame_rgba, (s[0], s[1]), (s[2], s[3]), (0, 255, 0, 255), 2, cv2.LINE_AA)
            else:
                pass

        else:
            self.trackerData.readImage(frame, self._is_ELSED_used)
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

                    cv2.line(frame_rgba, start, end, (0, 255, 0, 255), 2, cv2.LINE_AA)
                    # cv2.line(frame_rgba, start1, end1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame_rgba, str(lineIDs[idx]), un_line["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0, 255), 1, cv2.LINE_AA)

            # Draw tracked lines.
            if show_tracked:
                for idx, un_line in enumerate (un_lines):
                    if successes[idx] == -1:
                        continue # Ignore newly-detected lines

                    start, end = un_line["keyPoint"][1], un_line["keyPoint"][-1]
                    start1, end1 = un_line["StartPt"], un_line["EndPt"]

                    cv2.line(frame_rgba, start, end, (255, 0, 0, 255), 2, cv2.LINE_AA)
                    # cv2.line(frame_rgba, start1, end1, (255, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame_rgba, str(lineIDs[idx]), un_line["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0, 255), 1, cv2.LINE_AA)

                
            if self.nr_afterimage_lines > 0:

                lineRec = cur_img.lineRec

                # Declare constant that will be used for visualizing the lines.
                lengthDiff = 0.4 / self.nr_afterimage_lines

                for m in range(len(lineRec)):
                    lines = lineRec[m]
                    
                    # Show the afterimage using only the most recent line entries.
                    lines = lines[-min(len(lines), self.nr_afterimage_lines):]
                    lines = lines[::-1]

                    
                    for j, line in enumerate(lines[:-1]): #-1 to ignore the final line, which is the currently tracked line.

                        start, end = line['start'], line['end']

                        # Get inner points using parametric equations
                        s = int((1 - lengthDiff * j) * start[0] + lengthDiff * j * end[0]),\
                            int((1 - lengthDiff * j) * start[1] + lengthDiff * j * end[1])
                        
                        e = int((1 - lengthDiff * j) * end[0] + lengthDiff * j * start[0]),\
                            int((1 - lengthDiff * j) * end[1] + lengthDiff * j * start[1])
                        

                        cv2.line(frame_rgba, s, e, (colors[j][2], colors[j][1], colors[j][0], 255), 1, cv2.LINE_AA)
        
        frame_rgba = cv2.putText(frame_rgba, f'{int(round(Clock.get_fps()))}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 2, cv2.LINE_AA)
            
        # frame_rgba = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
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

    def negate_attribute(self, widget_instance: Widget, attribute_name: str, current_instance: Widget = None, *args):

        current_boolean_value = getattr(widget_instance, attribute_name)

        if type(current_boolean_value) == bool:
            setattr(widget_instance, attribute_name, not current_boolean_value)
            if current_instance is not None:
                if hasattr(current_instance, 'alternate_icon'):
                    # Swap icons.
                    current_instance.icon, current_instance.alternate_icon = current_instance.alternate_icon, current_instance.icon
        else:
            raise TypeError(f'Expected {current_boolean_value} to be of type {bool}.'
                            f'{current_boolean_value} is of type {type(current_boolean_value)} instead.')
        
    def dependence_negate_attribute(
        self, dependent_widget_instance: Widget,
        change_attribute_name: str, check_attribute_name: str,
        check_value: bool, set_value: bool,
        current_instance: Widget = None
    ):
        if getattr(dependent_widget_instance, check_attribute_name) == check_value:
            change_current_value = getattr(dependent_widget_instance, change_attribute_name)

            # Negate the attribute's valueonly in the case where
            # the change will result in the wanted`set_value`.
            if change_current_value == (not set_value):
                self.negate_attribute(dependent_widget_instance, change_attribute_name, current_instance)




class MixedRealityApplicationLayout(MDFloatLayout):
    def slider_callback(self):

        self.ids.camera.nr_afterimage_lines = int(self.ids.afterimage_counter.value)
        return True

class MyApp(MDApp):
    def build(self):
        # Clock.schedule_interval(lambda dt: print(Clock.get_fps()), 1)
        return MixedRealityApplicationLayout()

if __name__ == '__main__':
    MyApp().run()
