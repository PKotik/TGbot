import telebot
import bcrypt
from flask import Flask, request

from enum import Enum

class Status(Enum):
    NON = 0
    REG = 1
    AUT = 2
    PRE = 3

bot = telebot.TeleBot("7089479390:AAEHOQekHqFQe12gjEy5Emsb1Bo1FNZ_QXM")

app = Flask(__name__)


def myhash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def isadminToStr(chat):
    if (type(chat) is Admin):
        return "ADMIN"
    else:
        return "USER"

def isadmin(chat):
    if (type(chat) is Admin):
        return True
    else:
        return False


class Chat:
    def __init__(self, id):  # Регистарция
        self.__isaut = False
        self.__id = id
        self.__status=Status.REG
        self.__count_reqests = 0
        bot.send_message(self.__id, "Придумайте пароль 🤫")

    def getid(self):
        return self.__id
    def getcount_reqests(self):
        return self.__count_reqests
    def getstatus(self):
        return self.__status

    def registration(self, password):
        password = myhash(password)
        self.__password = password
        bot.send_message(self.__id, "Аккаунт зарегестрирован 😇")
        self.__isaut = True
        self.__status=Status.NON

    def logout(self, message):
        if self.__isaut:
            self.__isaut = False
            bot.send_message(self.__id, "Вы успешно вышли из аккаунта 😪😮‍💨")
        else:
            bot.reply_to(message, "Вы не авторизированы 😭")

    def wait_authorization(self, message):
        if self.__isaut==True:
            bot.reply_to(message, "Вы уже авторизированы 🤡")
        else:
            bot.send_message(self.__id, "Введите пароль 🤓")
            self.__status=Status.AUT

    def authorization(self,password):
        if bcrypt.checkpw(password.encode('utf-8'), self.__password):
            self.__isaut = True
            bot.send_message(self.__id, "Авторизация успешна 🥳🥳🥳")
        else:
            bot.send_message(self.__id, "Неверный пароль. Мда 😐")
        self.__status=Status.NON

    def wait_predict(self, message):
        if self.__isaut==False:
            bot.reply_to(message, "Вы не авторизированы 🤬")
        else:
            self.__status=Status.PRE
            bot.send_message(self.__id, "Пришли мне фоточку 😏")
    def predict(self, message):
        bot.send_message(message.chat.id, "Это временно не работает 🙈")
        self.__count_reqests+=1
        self.__status=Status.NON

first_amin = True

class Admin(Chat):

    def __init__(self, id_, status, count_reqests, password, isaut):
        self._Chat__id = id_
        self._Chat__status = status
        self._Chat__count_reqests = count_reqests
        self._Chat__password = password
        self._Chat__isaut = isaut
    def read_users(self):
        #print("Я читаю юзеров и колво их предсказаний, его id (какой-то) и уровень (админ или нет)")
        output=""
        for chat in chats:
            output+=f"id: {chat.getid()} <> status: {isadminToStr(chat)} <> count requests: {chat.getcount_reqests()}\n"
        bot.send_message(self.getid(), output)
    def del_user(self, id):
        #print("Я удаляю его")
        chats[:] = [chat for chat in chats if chat.getid() != id]
    def make_this_admin(self):
        self.__firstadmin = False
        print("Я делаю его админом")
    #admin = Admin.make_me_admin(chat)
    def ifirstadmin(self):
        return self.__firstadmin
    @staticmethod
    def make_me_admin(chat):
        return Admin.make_admin(chat)

    @classmethod
    def make_admin(cls, chat_obj):
        return cls(
            chat_obj._Chat__id,
            chat_obj._Chat__status,
            chat_obj._Chat__count_reqests,
            chat_obj._Chat__password,
            chat_obj._Chat__isaut
        )


chats = []

@bot.message_handler(commands=['register'])
def register(message):
    chat = Chat(message.chat.id)
    chats.append(chat)

@bot.message_handler(commands=['login'])
def login(message):
    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat==None:
        bot.send_message(message.chat.id, "Вы не существуете 🥶")
        return
    chat.wait_authorization(message)

@bot.message_handler(commands=['logout'])
def logout(message):
    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat==None:
        bot.send_message(message.chat.id, "Вы не существуете 😂")
        return
    chat.logout(message)

@bot.message_handler(commands=['predict'])
def logout(message):
    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat==None:
        bot.send_message(message.chat.id, "Вы не существуете 😈")
        return
    chat.wait_predict(message)

@bot.message_handler(commands=['admin'])
def admin(message):
    global first_amin 

    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat is None:
        bot.send_message(message.chat.id, "Вы не существуете 😈")
        return

    if not first_amin:
        bot.send_message(message.chat.id, "Поздно. Ха-ха-ха.")
        return

    admin_obj = Admin.make_me_admin(chat)
    first_amin = False

    index = chats.index(chat)
    chats[index] = admin_obj

    bot.send_message(message.chat.id, "Теперь вы админ 😎")

@bot.message_handler(commands=['users'])
def users(message):
    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat==None:
        bot.send_message(message.chat.id, "Вы не существуете 😈")
        return
    if not(type(chat) is Admin):
        bot.send_message(message.chat.id, "Вы не админ 🤮")
        return
    chat.read_users()

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def answer(message):
    chat = next((b for b in chats if b.getid() == message.chat.id), None)
    if chat==None:
        bot.send_message(message.chat.id, "Вы не существуете 😷")
        return
    elif chat.getstatus() == Status.REG and message.content_type == 'text':
        chat.registration(message.text)
        return
    elif chat.getstatus() == Status.AUT and message.content_type == 'text':
        chat.authorization(message.text)
        return
    elif (chat.getstatus() == Status.REG or chat.getstatus() == Status.AUT) and message.content_type != 'text':
        bot.reply_to(message, "Аахпхапхапх, сын фермера 🤠🤠, пароль - это текст!")
        return
    if chat.getstatus() == Status.PRE and message.content_type == 'photo':
        chat.predict(message)
        return
    elif chat.getstatus() == Status.PRE and message.content_type != 'photo':
        bot.reply_to(message, "Это не фото, вообще-то 🤨...")
        return
    else:
        bot.reply_to(message, "Чё сказал? 😑")
        return

@app.route('/', methods=['POST'])
def webhook():
    json_data = request.get_json()
    print("Получено обновление:", json_data)
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)