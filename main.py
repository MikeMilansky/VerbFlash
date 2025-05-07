import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from database import get_phrasal_verbs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a welcome message to the user when the /start command is issued.

    Args:
        update (Update): Incoming update containing the message and metadata.
        context (ContextTypes.DEFAULT_TYPE): Context object with additional information.
    """

    welcome_message = (
        "Hello, my dear friend!\n"
        "Приветствуем Вас в нашем небольшом чат-боте, который:\n"
        "☆ переводит фразовые глаголы\n"
        "☆ предоставляет примеры\n"
        "Приятной совместной работы!"
    )
    await update.message.reply_text(welcome_message)

async def show_random_phrasal_verb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a random phrasal verb and its applicable particles to the user.

    Retrieves a list of phrasal verbs from the database and selects one at random.
    Sends the selected verb and its particles in a formatted message. Offers the
    user an option to view detailed translations and examples through an inline button.

    Args:
        update (Update): The incoming update that triggered this handler.
        context (ContextTypes.DEFAULT_TYPE): The context object containing user data.

    Notes:
        - If no phrasal verbs are found in the database, an appropriate message is sent.
        - The user's selected particles are stored in context.user_data for further use.
    """

    phrasal_verbs = get_phrasal_verbs()
    if not phrasal_verbs: # no phrasal verbs case handler to pass a friednly message
        await update.message.reply_text('Нет фразовых глаголов в базе данных.')
        return

    random_verb = random.choice(phrasal_verbs)
    verb = random_verb['verb']
    particles = random_verb['phr_verbs']

    message = (
        f"<b>Фразовый глагол:</b> {verb}\n"
        f"<b>Применимые частицы:</b> {', '.join(particle['particle'] for particle in particles)}\n"
    )

    context.user_data['particles'] = particles
    await update.message.reply_text(message, parse_mode="HTML")

    keyboard = [[InlineKeyboardButton("Показать ответ", callback_data='show_answer')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Показать ответ?', reply_markup=reply_markup)

async def display_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the detailed answer for a phrasal verb.

    Retrieves the answer message from the user's stored particles and sends it as a reply to the user's query.

    Args:
        update (Update): The incoming update that triggered this handler.
        context (ContextTypes.DEFAULT_TYPE): The context object containing user data.
    """
    query = update.callback_query
    await query.answer()

    particles = context.user_data.get('particles', [])
    answer_message = ''.join(
        f"<b>{particle['verb']}</b> - {particle['translation']}\n\n"
        f"{particle['example'].replace(particle['verb'], f'<b>{particle['verb']}</b>')}\n\n"
        for particle in particles
    )

    await query.edit_message_text(text=answer_message, parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flash", show_random_phrasal_verb))
    app.add_handler(CallbackQueryHandler(display_answer, pattern="show_answer"))

    app.run_polling()

if __name__ == '__main__':
    main()
