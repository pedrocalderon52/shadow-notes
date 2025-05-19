import os
from wordcloud import WordCloud

CACHE_DIR = os.path.join(os.getcwd(), ".cache")
KEYLOG_FILE = os.path.join(CACHE_DIR, "ux_metrics.tmp")
WORDCLOUD_FILE = os.path.join(CACHE_DIR, "notes_wordcloud.png")

def generate_wordcloud():
    if not os.path.exists(KEYLOG_FILE):
        return
    with open(KEYLOG_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    if text.strip():
        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        wc.to_file(WORDCLOUD_FILE)
