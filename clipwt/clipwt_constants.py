import os

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ressources")
ICON_SIZE = (16, 16)
PLAY_ICON_PATH = os.path.join(image_path, "icon_play.png")
STOP_ICON_PATH = os.path.join(image_path, "icon_stop.png")
CLIP_ICON_PATH = os.path.join(image_path, "icon_clip.png")
CLEAR_ICON_PATH = os.path.join(image_path, "icon_clear.png")

class ClipAppStatus:

    START = 0x1
    STOP = 0x11
