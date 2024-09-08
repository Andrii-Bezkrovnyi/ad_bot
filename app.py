import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('bot_info.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Initialize the bot with the token from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


# Command processing function /start
async def start(update: Update, context):
    logging.info("Command /start received")
    await update.effective_message.reply_text("Welcome! Type /add_ad to create a new ad.")


async def add_ad_command(update: Update, context):
    logging.info("Command /add_ad received")
    ad_template = "###\nТекст оголошення\n###\nМісто\n###\nЦіна (число)"
    await update.effective_message.reply_text(
        text=f"Таким має бути оголошення:\n\n{ad_template}\n\nВідредагуй і відправ його",
        reply_markup=None)
    context.user_data['awaiting_ad'] = True


# Function for processing notifications of voicemails
async def handle_ad(update: Update, context):
    if 'awaiting_ad' in context.user_data and context.user_data['awaiting_ad']:
        ad_text = update.message.text
        logging.info(f"Received ad text: {ad_text}")
        lines = ad_text.split('\n')
        text = ''
        city = ''
        price = ''

        for line in lines:
            line = line.strip()  # It is cutting off your statements
            if line.startswith('###'):
                continue
            elif text == '':
                text = line
            elif city == '':
                city = line
            elif price == '':
                price = line

        # Валідація оголошення
        logging.info(f"Text: '{text}', City: '{city}', Price: '{price}'")

        text_length = len(text)
        word_count = len(text.split())
        text_valid = text_length > 0 and text_length < 2048
        price_valid = price.isdigit()

        logging.info(
            f"Text length: {text_length}, Word count: {word_count}, Text valid: {text_valid}, Price valid: {price_valid}")

        if text_valid and price_valid:
            try:
                price = int(price)
            except ValueError:
                await update.message.reply_text("Некоректна ціна")
                logging.error("Invalid price format")
                return

            # Збереження оголошення у файл
            date = datetime.now().strftime("%Y-%m-%d")
            user_id = update.message.from_user.id
            folder_name = f"{date}_{user_id}"
            os.makedirs(folder_name, exist_ok=True)
            file_name = "post.json"
            file_path = os.path.join(folder_name, file_name)

            ad_data = {
                "text": text,
                "city": city,
                "created_at": date,
                "tguser_id": user_id,
                "price": price
            }

            with open(file_path, 'w') as f:
                json.dump(ad_data, f, ensure_ascii=False)

            await update.message.reply_text("Оголошення збережено")
        else:
            await update.message.reply_text("Некоректне оголошення")
            logging.error("Invalid ad data")

        context.user_data['awaiting_ad'] = False


# Creating an application
app = ApplicationBuilder().token(TOKEN).build()

# Additional collections
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_ad", add_ad_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad))

# Run the bot
if __name__ == '__main__':
    app.run_polling()
