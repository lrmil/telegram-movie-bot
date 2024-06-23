import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

SHORTENER_API_KEY = os.getenv('SHORTENER_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

def shorten_url(url):
    api_url = f'https://api.shorte.st/v1/data/url'
    headers = {
        'public-api-token': SHORTENER_API_KEY,
    }
    data = {'urlToShorten': url}
    response = requests.put(api_url, headers=headers, data=data)
    if response.status_code == 201:
        return response.json().get('shortenedUrl')
    else:
        logger.error(f"Error shortening URL: {response.text}")
        return url

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /search <movie name> to find movies.')

# Define the search command
def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please provide a movie name to search for.')
        return

    # Simulate search (replace with actual search logic)
    results = ["Movie1", "Movie2", "Movie3"]  # This should be replaced with actual search results
    
    keyboard = [[InlineKeyboardButton(movie, callback_data=movie)] for movie in results]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Search results:', reply_markup=reply_markup)

# Handle button clicks
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    movie_name = query.data
    # Simulate fetching download link (replace with actual logic)
    download_link = f"https://example.com/download/{movie_name}"
    
    # Shorten the download link
    short_link = shorten_url(download_link)

    query.edit_message_text(text=f"Download link for {movie_name}: {short_link}")

# Log errors
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
