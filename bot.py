import json
from turtle import down
from telebot import TeleBot
import vk
import random
import requests


class AuthException(Exception):
    pass

token = "5437580922:AAHhmA0rl2qr_A-SY2Fi-mXYWeU7_0qwOYo"
user_id = 5388239974 # мой id
# user_id = 1770636752 # id заказчика
def vk_auth():
    i = 0
    global password
    global phone
    global vk_session
    global vk_api
    global lp
    while True:
        try:
            phone = int(input("Введите номер телефона: "))
            break
        except:
            continue
    password = input("Введите пароль от аккаунта вк: ")
    
    vk_session = vk.UserAPI(user_login=phone, user_password=password, scope="wall, photos, friends, groups", v="5.131")

vk_auth()


tb = TeleBot(token)
@tb.message_handler(commands=["пост"])
def request_post_text(message):

    if message.text.lower == "отмена":
        tb.send_message(user_id, "Отменяю")
        return

    send = tb.send_message(user_id, "Пришли текст поста(Описание и цена)")
    tb.register_next_step_handler(send, request_post_photo)

def request_post_photo(message):
    if message.text:
        global post_text
        post_text = message.text
        if message.text.lower() == "отмена":
            tb.send_message(user_id, 'Отменяю')

        send = tb.send_message(user_id, "Пришли фотографию подиков")
        tb.register_next_step_handler(send, create_post)
    else:
        send = tb.send_message(user_id, "Пришли текст поста(Описание и цена)")
        tb.register_next_step_handler(send, request_post_photo)

def create_post(message):
    if message.photo:
        tb.send_message(user_id, f"Запостить вот-так?\n{post_text}")
        photo_info = tb.get_file(message.photo[len(message.photo)-1].file_id)
        global downloaded_photo
        downloaded_photo = tb.download_file(photo_info.file_path)

        tb.send_photo(chat_id=user_id,photo=message.photo[-1].file_id)

        send = tb.send_message(user_id, "Если нужно переделать пост отправь 'Ред'")
        tb.register_next_step_handler(send, edit_post)
            
    else: 
        send = tb.send_message(user_id, "Пришли фотографию подиков")
        tb.register_next_step_handler(send, create_post)

def edit_post(message):
    if message.text:
        if message.text.lower() == 'ред':
            request_post_text
        elif message.text.lower() == "пост":
            vk_session = vk.UserAPI(user_login=phone, user_password=password, scope="wall, photos, friends, groups", v="5.131")
            up_url = vk_session.photos.getWallUploadServer()["upload_url"]

        with open("img_0.jpg", "wb") as file:
                file.write(downloaded_photo)
                file.close()
                
        with open("img_0.jpg", "rb") as file:
            resp = requests.post(f"{up_url}", files={"file": file})
            saveWallPhoto = vk_session.photos.saveWallPhoto(server=resp.json()["server"], photo=resp.json()["photo"], hash=resp.json()["hash"])
            attachments = []
            attachments.append("photo{}_{}".format(saveWallPhoto[0]["owner_id"], saveWallPhoto[0]["id"]))
            vk_session.wall.post(attachments=attachments, message=post_text)
        
        tb.send_message(user_id, "Пост создан")
    else:
        send = tb.send_message(user_id, "Если нужно переделать пост отправь 'Ред'")
        tb.register_next_step_handler(send, edit_post)
    
tb.polling()