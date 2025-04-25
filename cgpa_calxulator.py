import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Initialize empty DataFrame
grades_df = pd.DataFrame(columns=["Course", "Grade", "Unit", "Point"])

grade_points = {
    'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0
}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I can calculate your CGPA. Use:\n"
        "/add <course> <grade> <unit>\n"
        "/calculate\n"
        "/reset"
    )

# Add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global grades_df
    try:
        course, grade, unit = context.args
        grade = grade.upper()
        unit = int(unit)

        if grade not in grade_points:
            await update.message.reply_text("Invalid grade. Use A-F.")
            return

        point = grade_points[grade]
        new_row = {"Course": course, "Grade": grade, "Unit": unit, "Point": point}
        grades_df = grades_df.append(new_row, ignore_index=True)

        await update.message.reply_text(f"Added: {course} - {grade} ({unit} units)")

    except Exception as e:
        await update.message.reply_text("Usage: /add <course> <grade> <unit>")

# Calculate CGPA
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if grades_df.empty:
        await update.message.reply_text("You haven't added any courses yet.")
        return

    grades_df["Total"] = grades_df["Unit"] * grades_df["Point"]
    total_points = grades_df["Total"].sum()
    total_units = grades_df["Unit"].sum()
    cgpa = total_points / total_units

    await update.message.reply_text(f"Your CGPA is: {cgpa:.2f}")

# Reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global grades_df
    grades_df = pd.DataFrame(columns=["Course", "Grade", "Unit", "Point"])
    await update.message.reply_text("All records cleared.")

# Main bot setup
app = ApplicationBuilder().token("7375279797:AAGcdcEPnZ2LTXejft38nMQHK9nAY8spDlg").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("calculate", calculate))
app.add_handler(CommandHandler("reset", reset))

app.run_polling()
