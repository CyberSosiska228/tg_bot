import telebot
import os
import random
import subprocess
import time


f = open("token", "r")
token = f.readlines()[0][:-1]
f.close()

bot = telebot.TeleBot(token)
os.system('mkdir log 2> /dev/null')


def download_file(file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = 0
    while True:
        file_name = random.randint(0, int(1e9))
        try:
            subprocess.check_output(f"ls log | grep {file_name}", shell=True)
        except (subprocess.CalledProcessError):
            break

    with open(f"log/{file_name}",'wb') as new_file:
        new_file.write(downloaded_file)


def download_files(message):
    i = message.json["photo"]
    download_file(i[-1]["file_id"])


def get_queue(message):
    empty = False
    try:
        all_img = subprocess.check_output("ls log", shell=True).decode()
    except:
        empty = True

    if (all_img == ""):
        empty = True

    if (empty):
        bot.send_message(message.from_user.id, "Queue is empty")
        return

    lst = all_img.split()
    for i in lst:
        bot.send_photo(message.from_user.id, photo=open(f"log/{i}", "rb"), caption=i)


def remove(message):
    msg = message.text.split()
    if (len(msg) > 2):
        bot.send_message(message.from_user.id, "Error...")
        return

    rm_num = 0
    try:
        rm_num = int(msg[1])
    except:
        bot.send_message(message.from_user.id, "Error...")
        return

    os.system(f"rm log/{rm_num} -f")
    bot.send_message(message.from_user.id, "Done...")



@bot.message_handler(content_types=["photo"])
def get_photo_messages(message):
    download_files(message)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if (message.text == "/queue"):
        get_queue(message)
    elif (message.text[:4] == "/rm "):
        remove(message)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        time.sleep(60)
