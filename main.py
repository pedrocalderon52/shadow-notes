from threading import Thread
from db import init_db
from gui import launch_gui
from utils.analytics_tracker import track_user_metrics

def init_background_services():
    Thread(target=track_user_metrics, daemon=True).start()
# How to make this daemon False work
if __name__ == "__main__":
    init_db()
    init_background_services()
    launch_gui()
