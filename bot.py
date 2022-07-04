import json
from telebot import TeleBot
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
import random

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
    global vk 
    global lp
    while True:
        try:
            phone = int(input("Введите номер телефона: "))
            break
        except:
            continue
    password = input("Введите пароль от аккаунта вк: ")
    while True:
        try:
            vk_session = vk_api.VkApi(phone, password, scope="wall, photos, friends, groups", api_version="5.131")
            vk_session.auth(token_only=True)
            vk = vk_session.get_api()
            lp = VkLongPoll(vk_session)
            break
        except Exception as e:
            print(e)
            print("Ошибка авторизации, повторная попытка...")
            i += 1
            if i == 5:
                raise AuthException("Ошибка авторизации, проверьте правильность пароля и номера телефона и попробуйте снова.")
            continue
            
vk_auth()


tb = TeleBot(token)
@tb.message_handler(commands=["Пост"])
def request_post_text(message):

    if message.text.lower == "отмена":
        tb.send_message(user_id, "Отменяю")
        return

    send = tb.send_message(user_id, "Пришли текст поста(Описание и цена)")
    tb.register_next_step_handler(send, request_post_photo)

def request_post_photo(message):
    global post_text
    post_text = message.text
    if message.text.lower() == "отмена":
        tb.send_message(user_id, 'Отменяю')

    send = tb.send_message(user_id, "Пришли фотографию подиков")
    tb.register_next_step_handler(send, create_post)

def create_post(message):
    if message.photo:
        print(f"{message.photo} - это фото")
        print(f"{post_text} - это текст поста")
        tb.send_message(user_id, f"Запостить вот-так?\n{post_text}")
        photo_info = tb.get_file(message.photo[len(message.photo)-1].file_id)
        print(photo_info)
        downloaded_photo = tb.download_file(photo_info.file_path)
        
        with open('img_' + str(random.randint(1,1000)) + ".jpg", 'wb') as new_file: 
            new_file.write(downloaded_photo) 

        tb.send_photo(chat_id=user_id,photo=message.photo[-1].file_id)

        send = tb.send_message(user_id, "Если нужно переделать пост отправь 'Ред'")
        tb.register_next_step_handler(send, edit_post)
            
    else: 
        send = tb.send_message(user_id, "Пришли фотографию подиков")
        tb.register_next_step_handler(send, create_post)

def edit_post(message):
    if message.text.lower() == 'ред':
        send = tb.send_message(user_id, "Пришли текст поста(Описание и цена)")
        tb.register_next_step_handler(send, request_post_text)
    elif message.text.lower() == "пост":
        pass
    
tb.polling()