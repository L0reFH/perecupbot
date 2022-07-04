import json
from telebot import TeleBot
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

token = "5437580922:AAHhmA0rl2qr_A-SY2Fi-mXYWeU7_0qwOYo"
user_id = 5388239974 # мой id
# user_id = 1770636752 # id заказчика


tb = TeleBot(token)
@tb.message_handler(commands=["Пост"])
def request_post_text(message):
    print(message.from_user.id)
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
        
tb.polling()