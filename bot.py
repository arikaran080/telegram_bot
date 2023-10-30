from dotenv import load_dotenv
from langchain_codes import handle_responces
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, Application,
                          ContextTypes, filters,
                          CommandHandler, MessageHandler,
                          CallbackQueryHandler, CallbackContext)
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = """

        I'm a English Conversation bot

        /new_chat - to start new conversation with the bot and it will delete the old conversations
        /help - to ask help how to talk to the bot
        /about - to know about the bot      
    
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, how can I help you")

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = """
    A conversation about "Section" can encompass a wide range of topics. 
    In a legal context, a section refers to a specific part of a statute or document. 
    In architecture, it could relate to a building's cross-sectional view. 
    In education, sections represent different classes or groups. 
    Music may involve discussing sections of a composition. 
    In everyday language, it could pertain to a portion of a book, a segment of a city, or a division in an organization. 
    Sections are everywhere, and the context determines their significance. 
    Whether legal, structural, educational, or otherwise, understanding and appropriately using sections is essential in various aspects of life.
    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_responces(new_text)
        else:
            return
    else:
        response: str = handle_responces(text)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update: {update}, caused error {context.error}")


if __name__ == '__main__':
    print('bot starting....')
    app = ApplicationBuilder().token(TOKEN).build()
    
    # commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('new_chat', new_chat))
    app.add_handler(CommandHandler('about', about))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)
    
    print('bot pooling....')
    app.run_polling() # poll+interval=3