import json
import os

POSTED_FILE = "posted_topics.json"

def load_posted_topics():
    if not os.path.exists(POSTED_FILE):
        return []
    try:
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def is_duplicate(topic_title):
    posted = load_posted_topics()
    return topic_title in posted

def mark_as_posted(topic_title):
    posted = load_posted_topics()
    if topic_title not in posted:
        posted.append(topic_title)
        with open(POSTED_FILE, "w", encoding="utf-8") as f:
            json.dump(posted, f, ensure_ascii=False, indent=2)
