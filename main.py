# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Translator-Bot-V2/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

FayasNoushad = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hai {}, Aku adalah bot translate yang dapat membantu anda dalam menerjemahkan teks.

Made by @xskull7
"""
HELP_TEXT = """
**Bagaimana cara Translate nya???**

1. Kamu tinggal kirim pesan yang ingin saya terjemahkan
2. Setelah itu akan ada daftar bahasa, kamu tinggal klik bahasa yang kamu mau translate
Contoh: aku ngirim pesan pakai bahasa indo, nanti bot nya akan menampilkan daftar bahasa
kemudian aku pilih english karena aku ingin terjemahkan dari Indonesian ke English

Made by @xskull7
"""
ABOUT_TEXT = """
- **Bot :** `Dimas Translate Bot`
- **Owner :** [Dimassrmdani](https://telegram.me/xskull7)
- **Channel :** [Friends](https://telegram.me/hanyabotferi)
- **Website :** [DarkSkull7 Site](https://darkskull7.my.to)
- **Blog :** [Python3](https://darkskull7.blogspot.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/hanyabotferi'),
        InlineKeyboardButton('Support', url='https://telegram.me/AnosSupport')
        ],[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
TRANSLATE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Website ⚙', url='https://darkskull7.my.to')
        ]]
    )
LANGUAGE_BUTTONS = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton("Malayam", callback_data="Malayalam"),
    InlineKeyboardButton("Tamil", callback_data="Tamil"),
    InlineKeyboardButton("Hindi", callback_data="Hindi")
    ],[
    InlineKeyboardButton("Kannada", callback_data="Kannada"),
    InlineKeyboardButton("Telugu", callback_data="Telugu"),
    InlineKeyboardButton("Marathi", callback_data="Marathi")
    ],[
    InlineKeyboardButton("Gujarat", callback_data="Gujarati"),
    InlineKeyboardButton("Oriya", callback_data="Odia"),
    InlineKeyboardButton("Benggala", callback_data="bn")
    ],[
    InlineKeyboardButton("Jerman", callback_data="German"),
    InlineKeyboardButton("Vietnam", callback_data="Vietnamese"),
    InlineKeyboardButton("Jepang", callback_data="Japanese")
    ],[
    InlineKeyboardButton("Punjabi", callback_data="Punjabi"),
    InlineKeyboardButton("Persia", callback_data="Persian"),
    InlineKeyboardButton("English", callback_data="English")
    ],[
    InlineKeyboardButton("Spanyol", callback_data="Spanish"),
    InlineKeyboardButton("Prancis", callback_data="French"),
    InlineKeyboardButton("Rusia", callback_data="Russian")
    ],[
    InlineKeyboardButton("Abrit", callback_data="hebrew"),
    InlineKeyboardButton("Indonesia", callback_data="Indonesian")
    ]]
)

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "close":
        await update.message.delete()
    else:
        message = await update.message.edit_text("`MenTerjemahkan...`")
        text = update.message.reply_to_message.text
        language = update.data
        translator = Translator()
        try:
            translate = translator.translate(text, dest=language)
            translate_text = f"**Diterjemahkan ke {language}**"
            translate_text += f"\n\n{translate.text}"
            if len(translate_text) < 4096:
                translate_text += "\n\nMade by @xskull7"
                await message.edit_text(
                    text=translate_text,
                    disable_web_page_preview=True,
                    reply_markup=TRANSLATE_BUTTON
                )
            else:
                with BytesIO(str.encode(str(translate_text))) as translate_file:
                    translate_file.name = language + ".txt"
                    await update.reply_document(
                        document=translate_file,
                        caption="Made by @xskull7",
                        reply_markup=TRANSLATE_BUTTON
                    )
                await message.delete()
        except Exception as error:
            print(error)
            await message.edit_text("Sesuatu yang salah. Kontak @xskull7.")

@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@FayasNoushad.on_message(filters.private & filters.text)
async def translate(bot, update):
    await update.reply_text(
        text="Pilih bahasa di bawah ini untuk diterjemahkan",
        disable_web_page_preview=True,
        reply_markup=LANGUAGE_BUTTONS,
        quote=True
    )
    
FayasNoushad.run()
