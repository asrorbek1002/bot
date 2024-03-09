from functools import wraps

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, \
    PicklePersistence
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton, ChatAction
import requests
import json
import datetime
import sqlite3

BOT_TOKEN = "6467590369:AAE80aQmHC5L6jRQ2wG3deFKWr-ezgA83vM"

ADMIN_ID = "6194484795"

API_KEY = "K82954460188957"


def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            user_id INTEGER UNIQUE
        );
    ''')
    conn.commit()
    conn.close()


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def add_user_to_db(user_id, first_name, last_name):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, first_name, last_name) 
        VALUES (?, ?, ?);
    ''', (user_id, first_name, last_name))
    conn.commit()
    conn.close()


@send_typing_action
def dollar(update, context):
    usd_kurs = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/'
    user = update.message.from_user.id

    response = requests.get(usd_kurs)
    data = json.loads(response.text)
    for item in data:
        kurs = str(item['Rate'])
        context.bot.send_message(chat_id=user, text=f"Hozirgi dollar kursi: {kurs}")


@send_typing_action
def euro(update, context):
    usd_kurs = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/EUR/'
    user = update.message.from_user.id

    response = requests.get(usd_kurs)
    data = json.loads(response.text)
    for item in data:
        kurs = str(item['Rate'])
        context.bot.send_message(chat_id=user, text=f"Hozirgi euro kursi: {kurs}")


@send_typing_action
def rubl(update, context):
    usd_kurs = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/RUB/'
    user = update.message.from_user.id

    response = requests.get(usd_kurs)
    data = json.loads(response.text)
    for item in data:
        kurs = str(item['Rate'])
        context.bot.send_message(chat_id=user, text=f"Hozirgi rubl kursi: {kurs}")


keyboard = [
    [
        KeyboardButton("💱Valyutа Kursi💱"),
        KeyboardButton("Rasmdan text ol")
    ],
    [
        KeyboardButton("⏱Vaqtlar⏱")
    ]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


@send_typing_action
def start(update, context):
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    add_user_to_db(user_id, first_name, last_name)
    update.message.reply_text(f'Salom {update.message.from_user.first_name}!\n\nMenulardan birini tanlang',
                              reply_markup=reply_markup)


@send_typing_action
def new_year(update, context):
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    remaining_time = new_year - now
    user_id = update.message.from_user.id
    days, seconds = divmod(remaining_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    response = (
        f"🎄 Yangi yilgacha {int(days)} kun, {int(hours)} soat, {int(minutes)} daqiqa va {int(seconds)} sekund qoldi \n\n"
        f"🎅 Kelayotgan yangi yilingiz bilan"
    )

    context.bot.send_message(chat_id=user_id, text=response)


@send_typing_action
def navroz(update, context):
    user_id = update.message.from_user.id
    now = datetime.datetime.now()
    march_21 = datetime.datetime(now.year, 3, 21)

    if now > march_21:
        # Eger bugun 21-Martdan keyin bo'lsa, kelayotgan yilga aylantiramiz
        march_21 = datetime.datetime(now.year + 1, 3, 21)

    remaining_time = march_21 - now

    days, seconds = divmod(remaining_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    response = (
        f"21-Martgacha {int(days)} kun, {int(hours)} soat, {int(minutes)} daqiqa va {int(seconds)} sekund qoldi \n\n"
        f"O'zbekiston uchun Yangi yil bayrami muborak."
    )

    context.bot.send_message(chat_id=user_id, text=response)


@send_typing_action
def yanvar(update, context):
    user = update.message.from_user.id
    now = datetime.datetime.now()
    january_14 = datetime.datetime(now.year, 1, 14)

    if now > january_14:
        # Eger bugun 14-Yanvardan keyin bo'lsa, kelayotgan yilga aylantiramiz
        january_14 = datetime.datetime(now.year + 1, 1, 14)

    remaining_time = january_14 - now

    days, seconds = divmod(remaining_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    response = (
        f"14-Yanvargacha {int(days)} kun, {int(hours)} soat, {int(minutes)} daqiqa va {int(seconds)} sekund qoldi \n\n"
        f"Barcha vatanimiz himoyachilarini bayramlari bilan tabriklayman."
    )

    context.bot.send_message(chat_id=user, text=response)


def mart(update, context):
    user = update.message.from_user.id
    now = datetime.datetime.now()
    march_8 = datetime.datetime(now.year, 3, 8)

    if now > march_8:
        # Eger bugun 8-Martdan keyin bo'lsa, kelayotgan yilga aylantiramiz
        march_8 = datetime.datetime(now.year + 1, 3, 8)

    remaining_time = march_8 - now

    days, seconds = divmod(remaining_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    response = (
        f"8-Martgacha {int(days)} kun, {int(hours)} soat, {int(minutes)} daqiqa va {int(seconds)} sekund qoldi \n\n"
        f"Xalqaro xotin-qizlar bayrami bilan barcha ayollarimizni chin qalbdan tabriklayman!."
    )
    context.bot.send_message(chat_id=user, text=response)


@send_typing_action
def convert_image(update, context):
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    file = newFile.file_path
    context.user_data['filepath'] = file
    keyboard = [[InlineKeyboardButton("Arabic", callback_data='ara'),
                 InlineKeyboardButton("Bulgarian", callback_data='bul'),
                 InlineKeyboardButton("Chinese", callback_data='chs')
                 ],
                [
                    InlineKeyboardButton("Croatian", callback_data='hrv'),
                    InlineKeyboardButton("Danish", callback_data='dan'),
                    InlineKeyboardButton("Dutch", callback_data='dut')
                ],
                [
                    InlineKeyboardButton("English", callback_data='eng'),
                    InlineKeyboardButton("Finnish", callback_data='fin'),
                    InlineKeyboardButton("French", callback_data='fre')
                ],
                [
                    InlineKeyboardButton("German", callback_data='ger'),
                    InlineKeyboardButton("Greek", callback_data='gre'),
                    InlineKeyboardButton("Hungarian", callback_data='hun')
                ],
                [
                    InlineKeyboardButton("Korean", callback_data='kor'),
                    InlineKeyboardButton("Italian", callback_data='ita'),
                    InlineKeyboardButton("Japanese", callback_data='jpn')
                ],
                [
                    InlineKeyboardButton("Polish", callback_data='pol'),
                    InlineKeyboardButton("Portuguese", callback_data='por'),
                    InlineKeyboardButton("Russian", callback_data='rus')
                ],
                [
                    InlineKeyboardButton("Spanish", callback_data='spa'),
                    InlineKeyboardButton("Swedish", callback_data='swe'),
                    InlineKeyboardButton("Turkish", callback_data='tur')
                ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Tillardan birini tanlang👇", reply_markup=reply_markup)


@send_typing_action
def vaqtlar(update, context):
    keyboard2 = [
        [
            KeyboardButton("🎄Yangi yil vaqti"),
            KeyboardButton("Navroz vaqti")
        ],
        [
            KeyboardButton("14-yanvar vaqti"),
            KeyboardButton("8-mart vaqti")
        ],
        [
            KeyboardButton("Asosiy menu")
        ]
    ]
    now = datetime.datetime.now()

    hours, seconds = divmod(now.hour * 3600 + now.minute * 60 + now.second, 3600)
    minutes, seconds = divmod(seconds, 60)

    response = f"Hozir: {now.day}-{now.month}-{now.year}\n"
    response += f"Soat: {int(hours)} soat, {int(minutes)} daqiqa, {int(seconds)} sekund.\n\n"
    response += "Kerakli menuni tanlang"
    update.message.reply_text(response,
                              reply_markup=ReplyKeyboardMarkup(keyboard2, one_time_keyboard=True, resize_keyboard=True))


@send_typing_action
def valyuta_kursi(update, context):
    keyboard3 = [
        [
            KeyboardButton("$ Dollar Kursi")
        ],
        [
            KeyboardButton("€ Euro Kursi"),
            KeyboardButton("Rubl Kursi")
        ],
        [
            KeyboardButton("Asosiy menu")
        ]
    ]
    reply_markup2 = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("kerakli tugmani tanlang", reply_markup=reply_markup2)


def button(update, context):
    filepath = context.user_data['filepath']
    query = update.callback_query
    query.answer()
    query.edit_message_text("Matn chiqarilmoqda...")
    data = requests.get(
        f"https://api.ocr.space/parse/imageurl?apikey={API_KEY}&url={filepath}&language={query.data}&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True")
    data = data.json()
    if data['IsErroredOnProcessing'] == False:
        message = data['ParsedResults'][0]['ParsedText']
        query.edit_message_text(f"{message}")
    else:
        query.edit_message_text(text="⚠️ Nimadir noto'g'ri bajarildi")


persistence = PicklePersistence('userdata')

def get_user_count():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count


def stats(update, context):
    count = get_user_count()
    update.message.reply_text(f'Bot foydalanuvchilari soni: {count}')



def photo_text(update, context):
    update.message.reply_text("Text chiqarmoqchi bo'lgan rasmni yuboring")


def text(update, context):
    text = update.message.text

    if text == "$ Dollar Kursi":
        dollar(update, context)
    elif text == "€ Euro Kursi":
        euro(update, context)
    elif text == "Rubl Kursi":
        rubl(update, context)
    elif text == "🎄Yangi yil vaqti":
        new_year(update, context)
    elif text == "Navroz vaqti":
        navroz(update, context)
    elif text == '14-yanvar vaqti':
        yanvar(update, context)
    elif text == '8-mart vaqti':
        mart(update, context)
    elif text == 'Asosiy menu':
        start(update, context)


def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex(r"^⏱Vaqtlar⏱"), vaqtlar))
    dp.add_handler(MessageHandler(Filters.regex(r"^💱Valyutа Kursi💱"), valyuta_kursi))
    dp.add_handler(MessageHandler(Filters.regex(r"^Rasmdan text ol"), photo_text))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()
    init_db()


if __name__ == '__main__':
    main()
