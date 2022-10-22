import cv2
from datetime import timedelta
import mediapipe as mp
import numpy as np
import pyfakewebcam
import subprocess
import time
from timeit import default_timer as timer

class Webcam:
    BLUR = 1

    def __init__(self, device_input, device_output, width, height):
        self._device_input = device_input
        self._device_output = device_output
        self._last_time = timer()
        self._last_state = False
        self.width = width
        self.height = height
        self._is_blur = True
        self._cam = pyfakewebcam.FakeWebcam(device_output, width, height)

        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_selfie_segmentation = mp.solutions.selfie_segmentation

        self._black = np.zeros((width,height,3), dtype=np.uint8)


    def isopen(self):
        current_time = timer()
        current_state = False
        if timedelta(seconds=current_time - self._last_time) > timedelta(seconds=2):
            self._last_time = current_time
            # Use command line fuser to list processes that uses device file
            usage = subprocess.Popen(["fuser", self._device_output], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=False)
            outs, _ = usage.communicate() # get the stdout
            # transform bytes array : remove the \n at end, to utf8 string, split by space withot the first item (it's the file path)
            outs = outs[:-1].decode("utf8").split(" ")[1:]
            # remove the empties items due to multiple space in the original output
            outs = list(filter(None, outs))
            
            # if one item is ending with the 'm' character is that a process is reading the file
            current_state = False
            for o in outs:
                if o[-1] == 'm':
                    current_state = True
                    break
            
        else:
            return self._last_state
        
        if current_state != self._last_state:
            if current_state == True:
                self._capture = cv2.VideoCapture(self._device_input)
                self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self._capture.set(cv2.CAP_PROP_FPS, 30.0)
            else:
                self._capture.release()

            self._last_state = current_state

        return current_state


    def set_background(self, background):
        if background == self.BLUR:
            self._is_blur = True
        else:
            self._is_blur = False
            self._bg_image = cv2.imread(background, cv2.IMREAD_UNCHANGED)
            self._bg_image = cv2.cvtColor(self._bg_image, cv2.COLOR_BGR2RGB)
            self._bg_image = cv2.resize(self._bg_image, (self.width, self.height), interpolation = cv2.INTER_AREA)


    def process(self, segmentation_level):
        if not self.isopen():
            img_cam = self._black
            time.sleep(1.0)
        else:
            with self._mp_selfie_segmentation.SelfieSegmentation(
                model_selection=0) as selfie_segmentation:

                if self._capture.isOpened():
                    success, image = self._capture.read()
                    if not success:
                        print("Ignoring empty camera frame.")
                        return

                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    if self._is_blur:
                        self._bg_image = cv2.blur(image, (27, 27))

                    results = selfie_segmentation.process(image)

                    condition = np.stack(
                    (results.segmentation_mask,) * 3, axis=-1) > segmentation_level

                    output_image = np.where(condition, image, self._bg_image)
                    
                    imghsv = cv2.cvtColor(output_image, cv2.COLOR_RGB2HSV).astype("float32")
                    (h, s, v) = cv2.split(imghsv)
                    s = s*0.65
                    s = np.clip(s,0,255)
                    imghsv = cv2.merge([h,s,v])

                    img_cam = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2RGB)

        img_cam = cv2.resize(img_cam, (self.width, self.height), interpolation = cv2.INTER_AREA)
        self._cam.schedule_frame(img_cam)