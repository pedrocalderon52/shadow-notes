from threading import Thread as TH, Event
from views.gui import App
from db import DB
from utils.analytics_tracker import track_user_metrics

def init_background_services(stop_event):
    read = TH(target=track_user_metrics, args=(stop_event,))
    read.start()
    return read

if __name__ == "__main__":
    db: DB = DB()
    app = App(db)
    stop_event = Event()
    reader = init_background_services(stop_event)

    try:
        app.mainloop()
    finally:
        stop_event.set()  # Set flag to stop the background thread
        reader.join()     # 