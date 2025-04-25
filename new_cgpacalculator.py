from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

# States
MENU, GRADE_INPUT = range(2)

# Custom keyboard
menu_keyboard = [
    [KeyboardButton("Calculate CGPA")],
    [KeyboardButton("Help"), KeyboardButton("Cancel")]
]
markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to CGPA Calculator Bot!\nChoose an option from the menu:",
        reply_markup=markup
    )
    return MENU

# Menu options
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text

    if choice == "Calculate CGPA":
        await update.message.reply_text(
            "Send your grades and credits like this:\n\n"
            "`4.0 3, 3.7 4, 3.0 2`",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
        return GRADE_INPUT

    elif choice == "Help":
        await update.message.reply_text(
            "To calculate CGPA:\nEnter each course's GPA and credit like this:\n"
            "`4.0 3, 3.7 4, 3.0 2`\n\nType 'Cancel' to return to menu.",
            parse_mode='Markdown'
        )
        return MENU

    elif choice == "Cancel":
        await update.message.reply_text("Returning to main menu...", reply_markup=markup)
        return MENU

    else:
        await update.message.reply_text("Please choose a valid option from the menu.")
        return MENU

# Calculate CGPA
async def calculate_cgpa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        entries = update.message.text.split(',')

        total_points = 0
        total_credits = 0

        for entry in entries:
            gpa_str, credit_str = entry.strip().split()
            gpa = float(gpa_str)
            credit = float(credit_str)

            total_points += gpa * credit
            total_credits += credit

        cgpa = total_points / total_credits
        await update.message.reply_text(
            f"Your CGPA is: {round(cgpa, 2)}",
            reply_markup=markup
        )
        return MENU

    except Exception:
        await update.message.reply_text(
            "Invalid format! Please follow this:\n`4.0 3, 3.7 4, 3.0 2`",
            parse_mode='Markdown'
        )
        return GRADE_INPUT

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Back to main menu.", reply_markup=markup)
    return MENU

# Main
if __name__ == '__main__':
    TOKEN = "7375279797:AAGcdcEPnZ2LTXejft38nMQHK9nAY8spDlg"

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            GRADE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_cgpa)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()