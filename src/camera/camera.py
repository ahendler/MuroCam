import ffmpeg
import cv2
import shutil
import time

class Camera:
    def __init__(self, username, password, ip):
        self.username = username
        self.password = password
        self.ip = ip
        self.input = ffmpeg.input(f'rtsp://{self.username}:{self.password}@{self.ip}:554/onvif1',
                                  rtsp_transport='udp', buffer_size='8M')

    def take_picture(self):
        filename = str(int(time.time_ns() / 1000000)) + '.jpg'
        output = ffmpeg.output(self.input, filename, r=10,
                                     max_delay='500000', loglevel='quiet', vframes=1, y=None)
        try:
            ffmpeg.run(output)
        except ffmpeg.Error as e:
            pass
        return filename


    def get_frame(self, filename):
        return cv2.imread(filename)
