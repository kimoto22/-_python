import tkinter
from tkinter import ttk
import imageio
from PIL import ImageTk, Image
import time
import threading
from imageio.plugins.ffmpeg import FfmpegFormat

class Video():
    def __init__(self):
        format = FfmpegFormat(
            "ffmpeg",
            "Many video formats and cameras (via ffmpeg)",
            ".mov .avi .mpg .mpeg .mp4 .mkv .wmv .webm",
            "I",
        )
        imageio.formats.add_format(format,True)#webm に対応させる。(だいぶ強引に)
    def openfile(self, file_path,frame):
        self.frame = frame
        try:
            self.video = imageio.get_reader(file_path)
        except imageio.core.fetching.NeedDownloadError:
            imageio.plugins.avbin.download()
            self.video = imageio.get_reader(file_path)
    def play(self):
        self.video_thread = threading.Thread(target=self._stream)
        self.video_thread.setDaemon(True)
        self.video_thread.start()
    def stop(self):
        self.video_thread.stop()
    def _stream(self):
        start_time=time.time()
        sleeptime = 1/self.video.get_meta_data()["fps"]
        print(self.video.get_meta_data()["fps"])
        frame_now = 0
        for image in self.video.iter_data():
            frame_now = frame_now + 1
            if frame_now*sleeptime >= time.time()-start_time:
                frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                self.frame.config(image=frame_image)
                self.frame.image = frame_image
                time.sleep(sleeptime)
            else:
                pass