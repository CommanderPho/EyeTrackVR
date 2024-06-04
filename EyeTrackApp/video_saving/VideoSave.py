from pathlib import Path
from threading import Thread
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc

class VideoSave:
    """
    Class that continuously writes a frame to a video file using a dedicated thread.
    
    from EyeTrackApp.video_saving.VideoSave import VideoSave

    """

    def __init__(self, frame=None, gui_video_save_path: str='output_VideoSave_video.avi'):
        self.frame = frame
        self.stopped = False
        self.video_writer = None
        self.gui_video_save_path = gui_video_save_path
        
    def __del__(self):
        self.stopped = True
        # Release the video writer
        if self.video_writer is not None:
            self.video_writer.release()


    def _init_video_writer(self):
        if self.video_writer is None:
            ## The video writer should be able to read the `self.camera_output_outgoing` queue just the like algorithms do
            print(f'self.video_writer is None. Setting up VideoWriter:\n\tself.gui_video_save_path: {self.gui_video_save_path}')

            # ## Left
            # gui_should_save_video = self.config.settings.gui_should_save_video
            # gui_video_save_path = self.config.settings.gui_video_save_path
            
            # ## Right:
            # gui_should_save_video = self.config.settings.gui_should_save_video_right
            # gui_video_save_path = self.config.settings.gui_video_save_path_right

            gui_should_save_video: bool = True
            gui_video_save_path: str = gui_video_save_path

            print(f'\tgui_should_save_video: {gui_should_save_video}, gui_video_save_path: "{gui_video_save_path}"')
            # gui_should_save_video

            gui_video_save_path = Path(gui_video_save_path).resolve()
            gui_video_save_path = gui_video_save_path.with_suffix(suffix='.avi')
            print(f'\tgui_video_save_path: "{gui_video_save_path}"')            

            # gui_video_save_path = 'output_video.avi'

            # Instantiate the video writer when the first frame is captured
            # frame_height, frame_width = image.shape[:2]
            frame_height = 240
            frame_width = 240
            fps = 15
            fourcc = VideoWriter_fourcc(*'MJPG')  # 'XVID' for avi, 'mp4v' for mp4
            # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            print(f'\tMaking new VideoWriter with:\n\tfps: {fps} ({frame_width} x {frame_height})')
            # fps = max(fps, 15)
            self.video_writer = VideoWriter(gui_video_save_path, fourcc, fps, (frame_width, frame_height)) # , isColor=False


    def start(self):
        self._init_video_writer() ## initialize video writer
        Thread(target=self.write, args=()).start()
        return self

    def write(self):
        while not self.stopped:
            if self.video_writer is not None:
                self.video_writer.write(self.frame.astype('uint8')) # uses `self.frame`

            # cv2.imshow("Video", self.frame)
            # if cv2.waitKey(1) == ord("q"):
            #     self.stopped = True


    def stop(self):
        self.stopped = True
