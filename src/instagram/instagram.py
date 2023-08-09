from instagrapi import Client
import random
import datetime
import os
import pickle
from loguru import logger

class Instagram:
    def __init__(self, app_id, username, password):
        self.app_id = app_id
        self.username = username
        self.password = password

        # Check if the instagram_client.pickle file exists to avoid logging in every time
        if os.path.exists('instagram_client.pickle'):
            logger.info("Loading Instagram Client instance from file")
            with open('instagram_client.pickle', 'rb') as f:
                self.cl = pickle.load(f)
        else:
            logger.warning("Creating new Instagram Client instance")
            self.cl = Client()
            self.cl.login(username, password)
            with open('instagram_client.pickle', 'wb') as f:
                pickle.dump(self.cl, f)
    
    def post(self, image_path, caption=None):
        if caption is None:
            caption = self.generate_caption()
        self.cl.photo_upload(image_path, caption)
        logger.info(f"Image {image_path} posted")

    def generate_caption(self):
        emoji_face = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "😘", "😗", "😙", "😚", "☺️", "🙂", "🤗", "🤔", "🤭", "🤫", "🤥", "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "😌", "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕", "🤢", "🤮", "🥵", "🥶", "😵", "🤯", "🤠", "🥳", "😎", "🤓", "🧐", "😕", "😟", "🙁", "☹️", "😮", "😯", "😲", "😳", "🥺", "😦", "😧", "😨", "😰", "😥", "😢", "😭", "😱", "😖", "😞", "😓", "😩", "😫", "🥱", "😤", "😡", "😠", "🤬", "🤯", "😷", "🤒", "🤕", "🤢", "🤮", "🥴", "🥺"]
        emoji_food = ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶️", "🌽", "🥕", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🧆", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥", "🥮", "🥠", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮", "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🍯", "🥛", "🍼", "☕", "🍵", "🧃", "🥤", "🍶", "🍺", "🍻"]
        emoji_animal = ["🐶", "🐱", "🐭", "🐹", "🐰", "🐻", "🐼", "🐻‍❄️", "🐨", "🐯", "🦁", "🐮", "🐷", "🐽", "🐸", "🐵", "🙈", "🙉", "🙊", "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🕸️", "🦂", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🦣", "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦬", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮", "🐕‍🦺", "🐈", "🐈‍⬛", "🐓", "🦃", "🦚", "🦜"]
        emoji_malicious = ["👅", "👄", "🍌", "👀", "🍑", "🔥", "💣", "🐍", "👹", "👺", "👿", "💩", "🤡", "🌶️", "🍆", "🍼", "🥵", "💦", "🍩"] 
        
        # Get the current time
        now = datetime.datetime.now().time()
        # Check if it's between 7pm and 5am
        if now.hour >= 19 or now.hour <= 5:
            # If it is, choose 3 mischievous emojis at random
            caption_emojis = random.sample(emoji_malicious, 3)
        else:
            # If it's not, choose 3 emojis at random
            caption_emojis = random.sample(emoji_face, 1) + random.sample(emoji_food, 1) + random.sample(emoji_animal, 1)
        # Return the emojis as a string
        return ''.join(caption_emojis)