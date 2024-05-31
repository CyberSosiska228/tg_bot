import telebot
import time
import subprocess
import os
import random


f = open("token", "r")
token = f.readlines()[0][:-1]
f.close()

f = open("chat_id", "r")
send_chat_id = int(f.readlines()[0])
f.close()

bot = telebot.TeleBot(token)
wait = 15 * 60


def send(image):
    img = open(f"log/{image}", "rb")
    bot.send_photo(send_chat_id, img)


first = True
while (True):
    all_img = ""
    try:
        all_img = subprocess.check_output("ls log", shell=True).decode()
    except (subprocess.CalledProcessError):
        print()
        print("Waiting for images")
        time.sleep(wait)
        continue

    if (all_img == ''):
        print()
        print("Waiting for images")
        time.sleep(wait)
        continue

    if (not first):
        img = all_img.split()[0]
        send(img)
        os.system(f"rm log/{img}")

    first = False

    time_now = subprocess.check_output("date", shell=True).decode()[:-1]
    sleep_time = random.randint(7 * 60 * 60, 15 * 60 * 60)
    hours = sleep_time // (60 * 60)
    minutes = (sleep_time - hours * 60 * 60) // 60
    seconds = sleep_time - hours * 60 * 60 - minutes * 60
    print()
    s = str(time_now) + "\n" + "Wait:" + "\n" + f"Hours: {hours}\tMinutes: {minutes}\tSeconds: {seconds}"
    print(s)
    os.system(f"echo \"{s}\" > next_time")
    time.sleep(sleep_time)
