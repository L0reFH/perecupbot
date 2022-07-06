import json
import time
from telebot import TeleBot
import vk
import random
import requests


groups = [
    -62441045,
    -203102543,
    -184648211,
    -68829811,
    -204517084,
    -212824275,
    -157615038,
    -151598880,
    -146665911,
    -130150864,
    -134416509,
    -158969191,
    -146655979,
    -202176632,
    -199963188,
    -210879159,
    -203748128,
    -128118706,
    -147002621,
    -200896907,
    -207857905,
    -203303458,
    -204514980,
    -7241540,
    -208243426,
    -144614991,
    -200357122,
    -91335741,
    -156878704]


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

    while True:
        try:
            phone = int(input("Введите номер телефона: "))
            break
        except:
            continue
    password = input("Введите пароль от аккаунта вк: ")

    vk_session = vk.UserAPI(user_login=phone, user_password=password, scope="wall, photos, friends, groups", v="5.131", client_id=8203325)
    print("Бот успешно запущен!")
    print("Иди клепай свои объявления, шизик")


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
        photo_info = tb.get_file(message.photo[len(message.photo)-1].file_id)
        global downloaded_photo
        downloaded_photo = tb.download_file(photo_info.file_path)
        
        tb.send_message(user_id, "Проверь пост перед отправкой")
        tb.send_message(user_id, post_text)
        tb.send_photo(user_id, message.photo[-1].file_id)
        send = tb.send_message(user_id, "Если нужно переделать пост, пиши 'ред', если пост готов и его нужно запостить, пиши 'пост'")
        tb.register_next_step_handler(send, send_post)
        
    else: 
        send = tb.send_message(user_id, "Пришли фотографию подиков")
        tb.register_next_step_handler(send, create_post)

def send_post(message):
    if message.text:
        if message.text.lower() == 'ред':
            send = tb.send_message(user_id, "Пришли текст поста(Описание и цена)")
            tb.register_next_step_handler(send, request_post_photo)

        elif message.text.lower() == "пост":
            attachments = []
            vk_session = vk.UserAPI(user_login=phone, user_password=password, scope="wall, photos, friends, groups", v="5.131", client_id=8203325)
            up_url = vk_session.photos.getWallUploadServer()["upload_url"]
                
            
            with open("img_0.jpg", "wb") as file:
                file.write(downloaded_photo)
                file.close()
            
            # загрузка фото на сервер 
            with open("img_0.jpg", "rb") as file:
                resp = requests.post(f"{up_url}", files={"file": file})
                print(resp.json())
                saveWallPhoto = vk_session.photos.saveWallPhoto(server=resp.json()["server"], photo=resp.json()["photo"], hash=resp.json()["hash"])
                attachments = []
                attachments.append("photo{}_{}".format(saveWallPhoto[0]["owner_id"], saveWallPhoto[0]["id"]))
                

                for group in groups:
                    try: 
                        vk_session.wall.post(message=post_text, owner_id=group, attachments=attachments)
                        tb.send_message(user_id, f"Удачный пост в группу: https://vk.com/club{group*-1}")
                        time.sleep(1)
                        

                    except Exception as e:
                        print(e)
                        tb.send_message(user_id, f"Неудачный пост в группу: https://vk.com/club{group*-1}")
                        continue

                tb.send_message(user_id, "Работа окончена")
                return
    else:
        send = tb.send_message(user_id, "Если нужно переделать пост, пиши 'ред', если пост готов и его нужно запостить, пиши 'пост'")
        tb.register_next_step_handler(send, send_post)
    
tb.polling()