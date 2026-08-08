import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ----------------- CONFIGURATION -----------------
TOKEN = "8640663302:AAF-R9_t6ts-9tYKjq1jnka5qDGHBPNVyPY"
ADMIN_ID = 8204399238 

CHANNELS = ["@asif548Dotcom"]  
SITE_1_URL = "https://t.me/AIVerseXBot?start=0a483c71"  
SITE_2_URL = "https://telegram.me/sixsevenclub_bot/app?startapp=ref_d86d20a9"  
DEFAULT_BANNER = "https://i.ibb.co.com/ynRRSpYK/image.jpg" 
SUPPORT_USER = "@asifwh_26"

user_data_db = {}
# -------------------------------------------------

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_subscription(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_data_db:
        user_data_db[user_id] = {"coins": 0, "referrals": 0}
        
    is_subscribed = await check_subscription(user_id, context)
    
    # ইউজার জয়েন করা না থাকলে চ্যানেল ও সাইটগুলোর বাটন দেখাবে
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 আমাদের চ্যানেল", url=f"https://t.me/{CHANNELS[0].replace('@', '')}")],
            [InlineKeyboardButton("🚀 Bot 1", url=SITE_1_URL), InlineKeyboardButton("🎮 Bot 2", url=SITE_2_URL)],
            [InlineKeyboardButton("✅ Joined / Verify", callback_data="verify_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        caption_text = (
            "🎯 **WELCOME TO BOT!**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "  ❶ প্রথমে আমাদের চ্যানেলে জয়েন করুন\n"
            "  ❷ নিচের সাইটগুলোতে ক্লিক করুন\n"
            "  ❸ কাজ শেষ করে নিচে **Joined / Verify** এ চাপ দিন!"
        )
        
        try:
            await update.message.reply_photo(photo=DEFAULT_BANNER, caption=caption_text, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            await update.message.reply_text(caption_text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        # জয়েন করা থাকলে সরাসরি ড্যাশবোর্ড দেখাবে
        await send_dashboard(update, context)

async def send_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"🎉 **WELCOME TO DASHBOARD!**\n\n"
        f"আপনি সফলভাবে ভেরিফাই সম্পন্ন করেছেন। নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি বেছে নিন:"
    )
    
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton("👤 Profile"), KeyboardButton("🎁 Refer & Earn")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🛠️ Help Me")]
    ], resize_keyboard=True)
    
    if update.message:
        try:
            await update.message.reply_photo(photo=DEFAULT_BANNER, caption=text, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        try:
            await update.callback_query.message.reply_photo(photo=DEFAULT_BANNER, caption=text, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "verify_join":
        user_id = query.from_user.id
        is_subscribed = await check_subscription(user_id, context)
        
        if is_subscribed:
            try:
                await query.message.delete()
            except Exception:
                pass
            await send_dashboard(update, context)
        else:
            await query.answer("⚠️ আপনি এখনো চ্যানেলে জয়েন করেননি! দয়া করে জয়েন করে আবার ভেরিফাই করুন।", show_alert=True)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_id = user.id
    
    if user_id not in user_data_db:
        user_data_db[user_id] = {"coins": 0, "referrals": 0}
        
    data = user_data_db[user_id]
    
    if text == "👤 Profile":
        profile_msg = (
            f"👤 **USER PROFILE**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ **Name:** {user.first_name}\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"💰 **Balance:** {data['coins']} Coins\n"
            f"👥 **Total Referrals:** {data['referrals']}"
        )
        await update.message.reply_text(profile_msg, parse_mode="Markdown")
        
    elif text == "🎁 Refer & Earn":
        referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
        refer_msg = (
            f"🎁 **REFER & EARN**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"বন্ধুদের সাথে শেয়ার করুন এবং কয়েন আর্ন করুন!\n\n"
            f"🔗 **Your Refer Link:**\n`{referral_link}`"
        )
        await update.message.reply_text(refer_msg, parse_mode="Markdown")
        
    elif text == "💳 Withdraw":
        if data['coins'] >= 10:
            await update.message.reply_text("✅ আপনার উইথড্র সফল হয়েছে! এডমিনের সাথে যোগাযোগ করুন।")
        else:
            await update.message.reply_text("⚠️ **Insufficient Balance!**\nআপনার অ্যাকাউন্টে পর্যাপ্ত কয়েন নেই। টাকা বা কয়েন তুলতে কমপক্ষে **১০ কয়েন** প্রয়োজন। বেশি বেশি রেফার করুন!", parse_mode="Markdown")
            
    elif text == "🛠️ Help Me":
        help_msg = (
            f"🛠️ **SUPPORT & HELP**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"যেকোনো প্রয়োজনে সরাসরি যোগাযোগ করুন:\n"
            f"💬 Admin: {SUPPORT_USER}"
        )
        await update.message.reply_text(help_msg, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    
    print("🤖 Bot is running smoothly...")
    app.run_polling()

if __name__ == '__main__':
    main()