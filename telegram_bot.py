import os
from dotenv import load_dotenv
import logging
from prompt_templates import chat_template
from agent import query_engine
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from users.controller import User

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text(
        "Hello! I'm here to help you with your questions. Just type your query, and I'll do my best to assist!"
    )


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to user queries."""
    user_query = update.message.text
    user = update.message.from_user

    # Log the query for reference
    logger.info("Received query from %s: %s", user.first_name, user_query)

    # Here you can add your logic to handle and respond to queries

    user = User()
    # user.clear_chat_history(query.user_id)
    chat_history = user.get_chat_history(1)
    formatted_query = chat_template.format(user_query=user_query, history=chat_history)
    response = query_engine.query(formatted_query)

    # Send the response
    # response = f"Here’s an answer to your query: '{user_query}'"

    # Send the response
    await update.message.reply_text(response.response)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel any action and end the conversation if needed."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Conversation canceled. Let me know if you have any other questions!"
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()
    )

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))

    # Message handler for general queries
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
