from threading import Thread
from views.gui import App
from db import DB
from utils.analytics_tracker import track_user_metrics

def init_background_services():
    Thread(target=track_user_metrics, daemon=True).start()
# How to make this daemon False work
if __name__ == "__main__":
    db: DB = DB()

    app = App(db)
    app.mainloop()
