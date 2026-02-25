import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your bot. How can I help you?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    logger.info(f'Received message: {update.message.text}')
    await update.message.reply_text(f'You said: {update.message.text}')

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text('Sorry, I did not understand that command.')

if __name__ == '__main__':
    application = ApplicationBuilder().token('YOUR_TOKEN_HERE').build()

    # Command handler for /start
    application.add_handler(CommandHandler('start', start))

    # Message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Fallback handler for unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown))

    # Start the Bot
    application.run_polling()