import ffmpeg
import cv2
import shutil

class Camera:
    def __init__(self, username, password, ip):
        self.username = username
        self.password = password
        self.ip = ip
        self.input = ffmpeg.input(f'rtsp://{self.username}:{self.password}@{self.ip}:554/onvif1',
                                  rtsp_transport='udp', buffer_size='8M')

    def take_picture(self):
        output = ffmpeg.output(self.input, 'image.jpg', r=10,
                                     max_delay='500000', loglevel='info', vframes=1, y=None)
        try:
            ffmpeg.run(output)
        except ffmpeg.Error as e:
            print(e.stderr)


    def get_frame(self):
        return cv2.imread('image.jpg')
