from modules.broadcast import broadcast_handler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import config
from modules.database import db
from modules.image_gen import create_welcome_card
import datetime

# --- Helpers ---
def is_admin(update: Update):
    if update.effective_chat.type == "private": return True
    user_status = update.effective_chat.get_member(update.effective_user.id).status
    return user_status in ['creator', 'administrator']

# --- Handlers ---
def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        text = (
            f"<b>✨ Welcome to {config.BOT_USERNAME}!</b>\n\n"
            f"I am a premium Group Management bot designed to make your community professional.\n\n"
            f"👤 <b>Owner:</b> <a href='tg://user?id={config.OWNER_ID}'>Admin</a>\n"
            f"🛠 <b>Status:</b> Operational"
        )
        keyboard = [
            [InlineKeyboardButton("➕ Add Me To Your Group", url=f"http://t.me/{config.BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("📖 Help", callback_data="help"), InlineKeyboardButton("🛠 Support", url=config.SUPPORT_URL)],
            [InlineKeyboardButton("👑 Owner", url=f"tg://user?id={config.OWNER_ID}")]
        ]
        update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

def on_added(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            # Bot added to group logic
            chat = update.effective_chat
            user = update.effective_user
            db.update_group(chat.id, chat.title, user.id)
            
            # Notify Owner
            owner_msg = (
                f"<b>🚀 New Group Added!</b>\n\n"
                f"<b>Title:</b> {chat.title}\n"
                f"<b>ID:</b> <code>{chat.id}</code>\n"
                f"<b>Added By:</b> {user.first_name} ({user.id})\n"
                f"<b>Time:</b> {datetime.datetime.now()}"
            )
            context.bot.send_message(config.OWNER_ID, owner_msg, parse_mode=ParseMode.HTML)
            
            # Intro in Group
            update.message.reply_text(
                "<b>Thanks for adding me!</b>\n\nPlease promote me to <b>Admin</b> with 'Send Messages' and 'Delete Messages' permissions to function correctly.",
                parse_mode=ParseMode.HTML
            )
        else:
            # New Member Welcome Logic
            group_data = db.get_group(update.effective_chat.id)
            welcome_template = group_data[2] if group_data else "Welcome {name}!"
            
            caption = welcome_template.format(
                name=member.first_name,
                username=f"@{member.username}" if member.username else member.first_name,
                id=member.id,
                group=update.effective_chat.title
            )
            
            img_path = create_welcome_card(member.first_name)
            
            keyboard = [[
                InlineKeyboardButton("🛠 Support", url=config.SUPPORT_URL),
                InlineKeyboardButton("📢 Updates", url=config.UPDATES_URL)
            ]]
            
            with open(img_path, 'rb') as photo:
                update.message.reply_photo(photo, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

# --- Admin Commands ---
def set_welcome(update: Update, context: CallbackContext):
    if not is_admin(update): return
    text = " ".join(context.args)
    if not text:
        return update.message.reply_text("Usage: `/setwelcome Hello {name}!`")
    db.set_welcome(update.effective_chat.id, text)
    update.message.reply_text("✅ Custom welcome message saved!")

def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != config.OWNER_ID: return
    msg = " ".join(context.args)
    # logic to iterate through db.groups and send message
    update.message.reply_text("Broadcast started...")

# --- Main ---
def main():
    updater = Updater(config.BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("broadcast", broadcast_handler))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setwelcome", set_welcome))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, on_added))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
