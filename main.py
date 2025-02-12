import json
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

DATA_FILE = "events.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"events": [], "votes": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as file: 
        return json.load(file)
    
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dumps(data, file, indent=4, ensure_ascii=False)

def add_event(name, discription):
    data = load_data()
    event_id = len(data["events"]) + 1
    data["events"].append({
        "id": event_id, 
        "name": name,
        "discription": discription
    })
    save_data(data)

def get_events():
    data = load_data()
    return data["events"]

