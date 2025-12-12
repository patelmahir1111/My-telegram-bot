#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ---------------- CONFIG ----------------
BOT_TOKEN = "8535225144:AAEXb9bjLNTLJ_OVBPmo3VadHeSxCYvMy_s"        # ← replace
ADMIN_ID = 8095198308             # ← replace with your telegram numeric ID
# ----------------------------------------

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! This is DM Bot.\n"
        "Send me any message and I will deliver it to the admin."
    )

# Forward all messages to admin
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # Tag user info
    header = f"📩 *New message from:* {user.first_name}\n"
    header += f"🆔 *User ID:* `{user.id}`\n"
    header += "━━━━━━━━━━━━━━\n"

    try:
        # Forward message + header
        await context.bot.send_message(chat_id=ADMIN_ID, text=header, parse_mode="Markdown")
        await msg.forward(ADMIN_ID)
    except Exception as e:
        print("Failed to forward:", e)

    await update.message.reply_text("📨 Your message has been sent to the admin.")

# Admin reply handler
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin replies using: /reply <user_id> message_text"""
    try:
        parts = update.message.text.split(" ", 2)

        if len(parts) < 3:
            await update.message.reply_text("Usage: /reply <user_id> <message>")
            return

        user_id = int(parts[1])
        reply_text = parts[2]

        await context.bot.send_message(chat_id=user_id, text=f"📩 Admin replied:\n\n{reply_text}")
        await update.message.reply_text("✔ Reply sent to user.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", admin_reply))   # admin-only
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin))

    print("DM Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
