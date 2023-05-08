from instagrapi import Client

class Instagram:
    def __init__(self, app_id, username, password):
        self.app_id = app_id
        self.username = username
        self.password = password
        self.cl = Client()
    
    def post(self, image_path, caption):
        self.cl.photo_upload(image_path, caption)