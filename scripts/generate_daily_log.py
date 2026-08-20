#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# === CONFIGURATION ===
LOG_DIR = "daily-logs"
JSON_FILE = os.path.join(LOG_DIR, "latest.json")

# === FALLBACK DATA (in case APIs are down) ===
FALLBACK_QUOTE = {
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs"
}
FALLBACK_ZEN = "Keep it simple, stupid!"

# === FETCH FROM APIs ===
def fetch_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {"quote": data[0]["q"], "author": data[0]["a"]}
    except:
        pass
    return FALLBACK_QUOTE

def fetch_zen():
    try:
        response = requests.get("https://api.github.com/zen", timeout=5, headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return FALLBACK_ZEN

# === GENERATE DAILY MARKDOWN ===
now = datetime.now()
today = now.strftime("%Y-%m-%d")
timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

filename = os.path.join(LOG_DIR, f"{today}.md")

quote = fetch_quote()
zen = fetch_zen()

content = f"""# Daily Development Log

**Date:** {today}

---

## 💡 Quote of the Day
> *"{quote['quote']}"*  
> — **{quote['author']}**

---

## 🧠 Developer Zen
> {zen}

---

## 📝 Today's Learning
- Reviewed Git and GitHub Actions
- Automated daily logging with Python
- Explored API integration for real-world data

---
_Log generated at: {timestamp}_
"""

# Write the markdown file
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

# Update the latest.json file
data = {
    "date": today,
    "quote": quote['quote'],
    "author": quote['author'],
    "zen": zen,
    "file": filename,
    "generated_at": timestamp
}
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Daily log generated: {filename}")
print(f"✅ Latest JSON updated: {JSON_FILE}")
