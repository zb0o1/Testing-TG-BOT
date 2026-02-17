from telegram import Update, ParseMode
from telegram.ext import CallbackContext
import config
from modules.database import db

def broadcast_handler(update: Update, context: CallbackContext):
    # 🔐 Owner only
    if update.effective_user.id != config.OWNER_ID:
        return update.message.reply_text("❌ This command is only for the bot owner.")

    if not context.args:
        return update.message.reply_text(
            "Usage:\n/broadcast <message>"
        )

    message = " ".join(context.args)

    groups = db.get_all_groups()
    sent = 0
    failed = 0

    for (chat_id,) in groups:
        try:
            context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            sent += 1
        except Exception:
            failed += 1

    update.message.reply_text(
        f"✅ <b>Broadcast Finished</b>\n\n"
        f"📤 Sent: <b>{sent}</b>\n"
        f"❌ Failed: <b>{failed}</b>",
        parse_mode=ParseMode.HTML
    )
