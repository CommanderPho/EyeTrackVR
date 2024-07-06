from threading import Thread, Lock
import cv2
from pathlib import Path
from cv2 import VideoWriter, VideoWriter_fourcc

class VideoSave:
    def __init__(self, frame=None, width=240, height=240, fps=15, save_path='output_video.avi'):
        self.width = width
        self.height = height
        self.fps = fps
        self.save_path = Path(save_path).with_suffix('.avi').resolve()
        self.frame = frame
        self.stopped = False
        self.lock = Lock()
        self.video_writer = None
        self._init_video_writer()

    def __del__(self):
        self.stop()

    def _init_video_writer(self):
        fourcc = VideoWriter_fourcc(*'MJPG')
        self.video_writer = VideoWriter(str(self.save_path), fourcc, self.fps, (self.width, self.height))
        
    def start(self):
        Thread(target=self.write, args=()).start()
        return self

    def update_frame(self, new_frame):
        with self.lock:
            self.frame = new_frame.copy()

    def write(self):
        while not self.stopped:
            with self.lock:
                if self.frame is not None:
                    try:
                        self.video_writer.write(self.frame)
                    except Exception as e:
                        print(f'Error writing frame: {e}')
                        self.stop()

    def stop(self):
        with self.lock:
            self.stopped = True
            if self.video_writer is not None:
                self.video_writer.release()

