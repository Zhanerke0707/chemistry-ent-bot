from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN
from db import init_db, update_progress
from openai_api import explain_answer
import json, random

init_db()

with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

def get_keyboard(options):
    return ReplyKeyboardMarkup([[opt] for opt in options], one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для подготовки к ЕНТ по химии. Напиши /topics чтобы выбрать тему теста."
    )

async def topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери тему:",
        reply_markup=get_keyboard(list(QUESTIONS.keys()))
    )

async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    if topic not in QUESTIONS:
        await update.message.reply_text("Пожалуйста, выбери тему из списка командой /topics.")
        return
    question = random.choice(QUESTIONS[topic])
    context.user_data["current"] = (question, topic)
    await update.message.reply_text(question["question"], reply_markup=get_keyboard(question["options"]))

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    if "current" not in context.user_data:
        await update.message.reply_text("Напиши /topics чтобы начать тестирование.")
        return

    question, topic = context.user_data["current"]
    correct_answer = question["answer"]
    correct = 1 if user_answer == correct_answer else 0
    update_progress(update.message.from_user.id, topic, correct)
    explanation = explain_answer(question["question"], user_answer, correct_answer)
    await update.message.reply_text(
        f"{'✅ Верно!' if correct else '❌ Неверно.'}\n\n{explanation}"
    )
    del context.user_data["current"]
    await topics(update, context)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("topics", topics))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic))
app.run_polling()
