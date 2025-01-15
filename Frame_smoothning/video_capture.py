import cv2
from threading import Thread
import numpy as np

class VideoCapture:
    def __init__(self, src=0, frame_width=1280, frame_height=720, preprocess=True):
        """
        Initialize the video capture object with optional preprocessing.
        """
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.preprocess = preprocess

        self.grabbed, self.frame = self.capture.read()
        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        """
        Continuously grab frames from the video stream in a separate thread.
        """
        while self.running:
            grabbed, frame = self.capture.read()
            if grabbed:
                if self.preprocess:
                    frame = self.preprocess_frame(frame)
                self.grabbed, self.frame = grabbed, frame

    def preprocess_frame(self, frame):
        """
        Preprocess the frame: resize and convert to grayscale if needed.
        """
        frame = cv2.resize(frame, (640, 360))  # Resize for faster processing
        return frame

    def read(self):
        """
        Return the latest frame and its status.
        """
        return self.grabbed, self.frame

    def release(self):
        """
        Stop the video stream and release resources.
        """
        self.running = False
        self.thread.join()
        self.capture.release()
