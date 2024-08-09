import cv2
from telebot import *
from telebot import types
from subprocess import run
import time
import os
import logging
from pyautogui import *
from datetime import datetime

# ---------------------------------
# SETTINGS
token = "" # Bot token

write_logs = False
file_logs = "logs.log"
mode_logs = "w"
format_logs = "%(asctime)s %(levelname)s %(message)s"

users_ids = [] # Insert here the IDs of users who are allowed to use the bot
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

def button1(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    if write_logs:
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
def button2(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    if write_logs:
    	current_datetime = datetime.now()
    	write_data_time = str(current_datetime)
    	print(write_data_time + " SCREENSHOT @" + str(message.from_user.username))
    	logging.info("SCREENSHOT @" + str(message.from_user.username))
    screenshot("screen.png")
    scre = open('screen.png', 'rb')
    bot.send_photo(message.chat.id, scre)

@bot.message_handler(func=lambda message: message.text == "⌨ Keyboard")
def button3(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("⌨ Enter")
    item32 = types.KeyboardButton("⌨ Backspace")
    item33 = types.KeyboardButton("⌨ Escape")
    item34 = types.KeyboardButton("⌨ Alt+Tab")
    item35 = types.KeyboardButton("⌨ Windows+L")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31, item32, item33, item34, item35,backb)
    bot.send_message(message.chat.id, "📁 Keyboard: Select option:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "⌨ Enter")
def button4(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    press("enter")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Backspace")
def button5(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    press("backspace")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Escape")
def button6(message):
    if not message.from_user.id in users_ids:
    	return None
    press("esc")
    bot.send_message(message.chat.id, "✅ Success!")

@bot.message_handler(func=lambda message: message.text == "⌨ Alt+Tab")
def button7(message):
    if not message.from_user.id in users_ids:
    	return None
    hotkey('alt', 'tab')
    bot.send_message(message.chat.id, "✅ Success!")
@bot.message_handler(func=lambda message: message.text == "⌨ Windows+L")
def button8(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    hotkey('win', 'l')
    bot.send_message(message.chat.id, "✅ Success!")
@bot.message_handler(func=lambda message: message.text == "🖱 Mouse")
def button11(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item31 = types.KeyboardButton("🖱 Click")
    item32 = types.KeyboardButton("🖱 Double click")    
    backb = types.KeyboardButton("◀ Back")
    markup.add(item31, item32,backb)
    bot.send_message(message.chat.id, "📁 Mouse: Select option:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "🖱 Click")
def button12(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    click()
@bot.message_handler(func=lambda message: message.text == "🖱 Double click")
def button13(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    doubleClick()
@bot.message_handler(func=lambda message: message.text == "📜 Logs")
def button14(message):
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
def button15(message):
    if not message.from_user.id in users_ids:
    	return None
    global rlgs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item63 = types.KeyboardButton("🌐 Language")
    backb = types.KeyboardButton("◀ Back")
    markup.add(item63,backb)
    bot.send_message(message.chat.id, "📁 Keyboard: Select option:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "🌐 Language")
def button16(message):
    global rlgs
    if not message.from_user.id in users_ids:
    	return None
    bot.send_message(message.chat.id, "🌐 Language will be soon...")
@bot.message_handler(func=lambda message: message.text == "◀ Back")
def button16(message):
    global rlgs
    start(message)
@bot.message_handler(content_types='text')
def message_reply(message1):
    if not message.from_user.id in users_ids:
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