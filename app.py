from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes,MessageHandler, filters
from scraper import get_price_by_code
from emoji import emojize
import re
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_bot")

main_keyboard = ReplyKeyboardMarkup(
    [["💵قیمت دلار"],["💶قیمت یورو"],["💵قیمت لیر ترکیه"],["💷قیمت پوند انگلیس"],["💰قیمت طلا و سکه"], ["📘راهنما"]],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(emojize("شروع ربات 🐟", language="alias"), callback_data="start_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(emojize("برای شروع، دکمه زیر رو بزنید 👇", language="alias"), reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  

    if query.data == "start_bot":
        await query.message.reply_text(
            " لطفاً یکی از گزینه‌ها رو انتخاب کن",
            reply_markup=main_keyboard
        )

async def handle_gold_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()

    code_map = {
        "geram18": "geram18", 
        "sekee": "sekee", 
        "nim": "nim",  
        "rob": "rob"   
    }

    label_map = {
        "geram18": "طلای ۱۸ عیار",
        "sekee": "سکه امامی",
        "nim": "نیم سکه",
        "rob": "ربع سکه"
    }

    data = query.data
    if data in code_map:
        await query.edit_message_text(emojize("⏳ در حال دریافت قیمت...", language="alias"))

        price = get_price_by_code(code_map[data])
        await query.edit_message_text(f"{label_map[data]} = {price} ریال")

def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"   
                           u"\U0001F300-\U0001F5FF"   
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002700-\U000027BF"  
                           u"\U0001F900-\U0001F9FF"  
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text).strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text =remove_emojis(update.message.text.strip())

        if text in ["قیمت دلار", "قیمت یورو", "قیمت لیر ترکیه", "قیمت پوند انگلیس"]:

            loading_msg = await update.message.reply_text(emojize("⏳ در حال دریافت قیمت...", language="alias"))

            price_codes = {
                "قیمت دلار": "price_dollar_rl",
                "قیمت یورو": "price_eur",
                "قیمت لیر ترکیه": "price_try",
                "قیمت پوند انگلیس": "price_gbp"
            }

            price = get_price_by_code(price_codes[text])
            await loading_msg.edit_text(f"{text} = {price} ریال")

        elif text == "راهنما":
            await update.message.reply_text("🤖برای دریافت قیمت روی دکمه مربوطه کلیک کن")

        elif text == "قیمت طلا و سکه": 
             keyboard = [
                 [InlineKeyboardButton("طلای 18 عیار", callback_data="geram18")],
                 [InlineKeyboardButton("سکه امامی", callback_data="sekee")],
                 [InlineKeyboardButton("نیم سکه", callback_data="nim")],
                 [InlineKeyboardButton("ربع سکه", callback_data="rob")]
                 ]
             reply_markup = InlineKeyboardMarkup(keyboard)
             await update.message.reply_text("یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=reply_markup)
            
    else:
        print("هیچ پیام متنی دریافت نشد.")



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_gold_buttons ,  pattern="^(geram18|sekee|nim|rob)$"))
app.add_handler(CallbackQueryHandler(handle_button , pattern="^start_bot$"))





print("robot is active")
app.run_polling()
