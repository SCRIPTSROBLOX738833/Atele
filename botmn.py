from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import random

TOKEN = "7506545250:AAHA3tkqKj4ZTtQgBDyMZkUMV2VeX_b3eKs"
TARGET_USERNAME = "m_858l"

QUESTIONS = [
    "تحب تلعب روبلوكس؟",
    "ايه أكتر ماب بتحبه في روبلوكس؟",
    "بتلعب امتى غالبًا؟"
]

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        print("حد دخل:", member.username)
        if member.username == TARGET_USERNAME:
            await context.bot.promote_chat_member(
                chat_id=update.effective_chat.id,
                user_id=member.id,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
                can_restrict_members=True
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{member.username} اتعمله ادمن"
            )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text.lower() if msg.text else ""
    
    if "اسئله" in text:
        question = random.choice(QUESTIONS)
        await msg.reply_text(f"سؤال ليك: {question}")

    if "هلا" in text:
        # هنا بدل سب مباشر ممكن نعمل حاجة كوميدية
        await msg.reply_text("يشيخ كل زق")

async def handle_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.reply_to_message:
        user_to_ban = msg.reply_to_message.from_user
        try:
            await context.bot.ban_chat_member(chat_id=msg.chat.id, user_id=user_to_ban.id)
            await msg.reply_text(f"{user_to_ban.username} اتطرد على ايد البوت")
        except:
            await msg.reply_text("مش قادر اطرده، البوت محتاج صلاحيات")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
app.add_handler(CommandHandler("ban", handle_ban))

app.run_polling()