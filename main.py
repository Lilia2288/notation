import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

DATA_FILE = "events.json"

def load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"events": [], "votes": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"events": [], "votes": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_event(name, description):
    data = load_data()
    event_id = len(data["events"]) + 1
    data["events"].append({
        "id": event_id, 
        "name": name,
        "description": description
    })
    save_data(data)

def get_events():
    data = load_data()
    return data["events"]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для управління нотатками.\n"
        "Опис команд: /add_event, /list_events, /help."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Команди:\n"
        "/start - запуск бота\n"
        "/help - виведе цей список\n"
        "/add_event <назва> <опис> - додає нову нотатку\n"
        "/list_events - покаже всі створені нотатки"
    )    
    await update.message.reply_text(help_text)

async def add_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    parts = message_text.split(" ", 2)
    if len(parts) < 3:
        await update.message.reply_text(
            "❌ Використання: /add_event <назва> <опис>\n"
            "Приклад: /add_event Вечірка 'О 20:00 у клубі'"
        )
        return 
    name = parts[1]
    description = parts[2]
    add_event(name, description)
    await update.message.reply_text("✅ Додано нову замітку")

async def list_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_events()
    if not events:
        await update.message.reply_text("ℹ️ Поки що немає нотаток.")
        return
    
    event_list = "\n".join([f"{e['id']}. {e['name']} - {e['description']}" for e in events])
    await update.message.reply_text(f"📌 Список нотаток:\n{event_list}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_event", add_event_command))
    app.add_handler(CommandHandler("list_events", list_events_command))
    
    print("Бот запущено...")
    app.run_polling()
