import telebot
import style_transfer

bot = telebot.TeleBot("1584217211:AAGzlG8MK1a5hLJhPz0POg1vuFItL5uZfeo")
im_num = 0
content_img = 0
style_img = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start.\n'
                                      'Для начала отправь фото, которое надо изменить.')


@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    print('\n\n')
    downloaded_file = bot.download_file(file_info.file_path)
    global im_num
    # with open("image.jpg" if im_num == 0 else "picasso.jpg", 'wb') as new_file:
    #     new_file.write(downloaded_file)
    if im_num == 0:
        global content_img
        content_img = style_transfer.image_loader(downloaded_file)
        bot.send_message(message.chat.id, 'Фото принято (Content)\n'
                                          'Отправь фото, стиль которого нужно применить.')
        im_num += 1
    else:

        global style_img
        style_img = style_transfer.image_loader(downloaded_file)
        bot.send_message(message.chat.id, 'Фото принято (Style)\n'
                                          'Отправь команду /photo, чтобы получить результат\n'
                                          'Внимание! Обработка фото может занять некоторое время (~15 мин).')
        im_num = 0


@bot.message_handler(commands=['photo'])
def send_photo(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    image = style_transfer.get_img(content_img, style_img)
    # img = open('output.jpg', 'rb')
    bot.send_photo(message.chat.id, image, reply_to_message_id=message.message_id)
    # img.close()


bot.polling()
