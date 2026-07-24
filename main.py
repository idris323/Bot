import asyncio
import sqlite3

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)


# توکن BotFather را اینجا قرار بده
TOKEN = "8913309887:AAGsD6Ye9EnD1MH9xQHaPPgssTgiZTDSC4w"

# آیدی عددی خودت را اینجا بگذار
ADMIN_ID = 8769505934


# دیتابیس
db = sqlite3.connect("shop.db", check_same_thread=False)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
product TEXT
)
""")


db.commit()



# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    menu = [
        [
            InlineKeyboardButton(
                "🛒 فروشگاه",
                callback_data="shop"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 سفارش‌های من",
                callback_data="myorders"
            )
        ]
    ]


    if update.effective_user.id == ADMIN_ID:
        menu.append(
            [
                InlineKeyboardButton(
                    "⚙️ مدیریت",
                    callback_data="admin"
                )
            ]
        )


    await update.message.reply_text(
        "👋 به فروشگاه خوش آمدید",
        reply_markup=InlineKeyboardMarkup(menu)
    )




# دکمه ها
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "shop":

        cursor.execute(
            "SELECT * FROM products"
        )

        products = cursor.fetchall()


        if not products:
            await query.edit_message_text(
                "❌ محصولی وجود ندارد"
            )
            return


        text = "🛍 محصولات:\n\n"

        keyboard = []


        for item in products:

            text += (
                f"📌 {item[1]}\n"
                f"💰 قیمت: {item[2]}\n\n"
            )


            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"خرید {item[1]}",
                        callback_data=f"buy_{item[1]}"
                    )
                ]
            )


        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif query.data.startswith("buy_"):

        product = query.data.replace(
            "buy_",
            ""
        )


        cursor.execute(
            "INSERT INTO orders(user_id,product) VALUES(?,?)",
            (
                query.from_user.id,
                product
            )
        )


        db.commit()


        await query.edit_message_text(
            "✅ سفارش شما ثبت شد"
        )




    elif query.data == "myorders":

        cursor.execute(
            "SELECT product FROM orders WHERE user_id=?",
            (query.from_user.id,)
        )


        orders = cursor.fetchall()


        if not orders:
            await query.edit_message_text(
                "سفارشی ندارید"
            )
            return


        text = "📦 سفارش‌های شما:\n\n"


        for order in orders:
            text += "• " + order[0] + "\n"


        await query.edit_message_text(text)




    elif query.data == "admin":

        await query.edit_message_text(
            "⚙️ پنل مدیریت\n\n"
            "/add نام محصول قیمت\n"
            "/orders"
        )





# اضافه کردن محصول
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    if len(context.args) < 2:
        await update.message.reply_text(
            "مثال:\n/add کتاب 100"
        )
        return


    name = context.args[0]
    price = context.args[1]


    cursor.execute(
        "INSERT INTO products(name,price) VALUES(?,?)",
        (
            name,
            price
        )
    )


    db.commit()


    await update.message.reply_text(
        "✅ محصول اضافه شد"
    )





# دیدن سفارش ها توسط ادمین
async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    cursor.execute(
        "SELECT * FROM orders"
    )


    data = cursor.fetchall()


    text = "📦 سفارش ها:\n\n"


    for item in data:

        text += (
            f"👤 {item[1]}\n"
            f"📦 {item[2]}\n\n"
        )


    await update.message.reply_text(text)





# اجرای سازگار با Python 3.14
async def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "add",
            add
        )
    )


    app.add_handler(
        CommandHandler(
            "orders",
            orders
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )


    await app.initialize()
    await app.start()

    await app.updater.start_polling()


    print("Shop Bot Started")


    while True:
        await asyncio.sleep(100)





if __name__ == "__main__":
    asyncio.run(main())