import telebot
from telebot import types
import sql
import random, time
from keys import BOT_TOKEN
import variables

bot = telebot.TeleBot('6929575904:AAG4VIXsq6Q3LqSkAum6Z-8Z_eCl-xsJtGw')


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if str(message.chat.id).startswith('-'):
        bot.reply_to(message, f'Эта команда доступна только в личных сообщениях с ботом!')
    else:
        sql.add_user_to_level(chat_id, user_id, username, first_name, last_name)
        bot.send_message(message.chat.id, f'🌟Добро пожаловать, {message.from_user.first_name}!\nВ этом боте вы сможете отслеживать свой прогресс по заданиям, а также вашу посещяемость.\nЧтобы начать напишите /menu')


@bot.message_handler(commands=['all'])
def handle_all(message):
    if not str(message.chat.id).startswith('-'):
        bot.reply_to(message, 'Упоминать всех возможно только в групповых чатах!')
    else:
        members = sql.get_chat_members(message.chat.id)
        message_text = ''
        count = 0
        for member in members:
            emoji = variables.emoji_list[random.randint(0, 45)]
            member_emoji = f'[{emoji}](tg://user?id={member})'
            if count % 5 == 0:
                message_text = message_text + '\n'
                message_text = message_text + f'{member_emoji}  '
                count += 1
            else:
                message_text = message_text + f'{member_emoji}  '
                count += 1

            if count % 15 == 0:
                bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
                message_text = ''
            else:
                pass

        if message_text != '':
            bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
        else:
            pass

@bot.message_handler(commands=['addlevel'])
def handle_addlevel(message):
    if sql.get_admin(message.from_user.id):
        if message.text[10:] == '':
            sql.add_level(message.from_user.id)
            bot.reply_to(message, 'Успешно добавлен уровень!')
        else:
            try:
                sql.add_level(message.text[10:])
                bot.reply_to(message, 'Успешно добавлен уровень!')
            except TypeError:
                bot.reply_to(message, 'ID Указан неверно!')
    else:
        bot.reply_to(message, 'Недостаточно прав!')

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    if str(message.chat.id).startswith('-'):
        bot.reply_to(message, 'Открывать меню возможно только в личных сообщениях с ботом!')
    else:
        if True:
            markup = types.InlineKeyboardMarkup(row_width=2)
            button_level = types.InlineKeyboardButton('🏆 Прогресс', callback_data='level')
            button_visits = types.InlineKeyboardButton('📅 Посещаемость', callback_data='visits')
            button_add = types.InlineKeyboardButton('➕ Добавить задание', callback_data='add')
            button_help = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
            markup.add(button_level, button_visits, button_add, button_help)

            bot.send_message(message.chat.id, f"🔥Добро пожаловать, {message.from_user.first_name}🔥", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_back = types.InlineKeyboardButton('< Назад', callback_data='back')
    markup.add(button_back)

    if call.data == 'back':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button_level = types.InlineKeyboardButton('🏆 Прогресс', callback_data='level')
        button_visits = types.InlineKeyboardButton('📅 Посещаемость', callback_data='visits')
        button_add = types.InlineKeyboardButton('➕ Добавить задание', callback_data='add')
        button_help = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
        markup.add(button_level, button_visits, button_add, button_help)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🔥Добро пожаловать, {call.from_user.first_name}🔥", reply_markup=markup)

    if call.data == 'level':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Ваш уровень: {sql.get_level(call.from_user.id)}', reply_markup=markup)

@bot.message_handler(commands=['exalo'])
def handle_rinat(message):
    while True:
        time.sleep(0.7)
        bot.send_message(message.chat.id, text=f'дебилы')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if str(chat_id).startswith('-'):
        sql.add_user_to_group(chat_id, user_id, username, first_name, last_name)
    else:
        sql.add_user_to_level(chat_id, user_id, username, first_name, last_name)

    if message.text.startswith('//code'):
        chat_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        warn_id = str(user_id) + ' ' + username
        if message.text == '//code ' + variables.admin_code:
            sql.add_admin(chat_id, user_id, username, first_name, last_name)
        else:
            with open('warn.txt', 'r+', encoding='utf-8') as file1:
                file_contents = file1.read()
                if warn_id not in file_contents.splitlines():
                    file1.write(warn_id + '\n')
                else:
                    pass

def main():
    print('Bot has been started!')
    print('Admin code: ' + variables.get_admin_code() + '\n')
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(1)


if __name__ == "__main__":
    main()
