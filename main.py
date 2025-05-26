from threading import Thread as TH
from views.gui import App
from db import DB
from utils.analytics_tracker import track_user_metrics

def init_background_services():
    read = TH(target=track_user_metrics)
    read.start()
    return read

if __name__ == "__main__":
    db: DB = DB()

    app = App(db)
    reader = init_background_services()

    try:
        app.mainloop()
    finally:
        # This will make sure the background thread is stopped when the app closes
        reader.join()