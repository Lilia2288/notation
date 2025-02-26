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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! я бот для управління нотатками "
        "Опис команд: /event, /add_event, /list_events, /help."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Команди:\n"
        "/start - запуск бота"
        "/help - виводе цей список"
        "/add_event - <ім’я> <опис> додає нову нотатку"
        "/list_events - покаже всі створенні нотатки"
    )    
    await update.message.reply_text(help_text)

async def add_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    parts = message_text.split(" ", 2)
    if len(parts) < 3:
        await update.message.reply_text(
            "використання: /add_event <назва> <опис> \n"
            "Приклад: /add_event Вечірка о 20:00 у клубі"
        )
        return 
    name = parts[1]
    discription = parts[2]
    add_event(name, discription)
    await update.message.reply_text(
        "✅ додана нова замітка"
    )

