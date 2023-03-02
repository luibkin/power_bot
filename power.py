import subprocess
import telebot
import config
import time

ntd = telebot.TeleBot(config.token)


############################# Handlers #########################################

@ntd.message_handler(commands=['start'])
def answer_help(message):
    keyboard_main = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text="PowerOff", callback_data='result1')
    button_2 = telebot.types.InlineKeyboardButton(text="Reboot", callback_data='result2')
    button_3 = telebot.types.InlineKeyboardButton(text="Restart MiniDLNA", callback_data='result3')
#    keyboard_main = [[button_1, button_2], [button_3]]
    keyboard_main.row_width = 2
    keyboard_main.add(button_1, button_2, button_3)
    ntd.send_message(message.chat.id, 'Press button!', reply_markup = keyboard_main)
        
#    if result.returncode == 0:
#        xx = "Done!"
#    else:
#        xx = "Cant turn it off!"
#    ntd.send_message(message.chat.id, xx)
@ntd.message_handler(content_types=['text', 'audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def answer_help(message):
    ntd.send_message(message.chat.id, "Для начала работы введите /start")

@ntd.callback_query_handler(func=lambda call: True)
def callback_from_main_button(call):
    if call.data == 'result1':
        result1 = subprocess.run (['/sbin/shutdown', '-h', '1'])

        if result1.returncode == 0:
            ntd.answer_callback_query(call.id, show_alert=True, text='Система выключится через 1 минуту.')
            time.sleep(57)
            ntd.send_message(call.message.chat.id, text = 'Выключаю систему')

    elif call.data == 'result2':
        result2 = subprocess.run (['/sbin/shutdown', '-r', '1'])
        if result2.returncode == 0:
            ntd.answer_callback_query(call.id, show_alert=True, text='Система перезагрузится через 1 минуту.')
            time.sleep(57)
            ntd.send_message(call.message.chat.id, text = 'Перезагружаю систему')


    elif call.data == 'result3':
        result3 = subprocess.run (['systemctl', 'restart', 'minidlna'])
        ntd.answer_callback_query(call.id, show_alert=True, text='MiniDLNA перезагружен')


if __name__ == '__main__':
    ntd.infinity_polling()
