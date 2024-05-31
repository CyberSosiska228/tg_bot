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
sleep_time_from = 7 * 60 * 60
sleep_time_to = 15 * 60 * 60
rebuild_cnt = 14

sleep_time_from = 10
sleep_time_to = 15
rebuild_cnt = 4


def rebuild():
    try:
        all_img = list(map(int, subprocess.check_output("ls log", shell=True).decode()[:-1].split()))
    except:
        return

    all_img.sort()

    pt = 0
    for i in all_img:
        try:
            imgs = list(map(int, subprocess.check_output("ls log", shell=True).decode()[:-1].split()))
        except:
            imgs = []
        while (pt in imgs):
            pt += 1
        os.system(f"mv log/{i} log/{pt}")


def send(image):
    img = open(f"log/{image}", "rb")
    bot.send_photo(send_chat_id, img)


cnt = 0
first = True
while (True):
    cnt += 1
    if (cnt == rebuild_cnt):
        rebuild()
        cnt = 0

    all_img = ""
    try:
        all_img = list(map(int, subprocess.check_output("ls log", shell=True).decode()[:-1].split()))
    except (subprocess.CalledProcessError):
        os.system(f"echo \"Waiting for images\" > next_time")
        time.sleep(wait)
        continue

    if (len(all_img) == 0):
        os.system(f"echo \"Waiting for images\" > next_time")
        time.sleep(wait)
        continue

    if (not first):
        all_img.sort()
        img = all_img[0]
        send(img)
        os.system(f"rm log/{img}")

    first = False
    time_now = subprocess.check_output("date", shell=True).decode()[:-1]
    sleep_time = random.randint(sleep_time_from, sleep_time_to)
    hours = sleep_time // (60 * 60)
    minutes = (sleep_time - hours * 60 * 60) // 60
    seconds = sleep_time - hours * 60 * 60 - minutes * 60
    s = str(time_now) + "\n" + "Wait:" + "\n" + f"Hours: {hours}\tMinutes: {minutes}\tSeconds: {seconds}"
    os.system(f"echo \"{s}\" > next_time")
    time.sleep(sleep_time)
