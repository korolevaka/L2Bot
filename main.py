from tgbot import dp, bot

# Запускаем бота
if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)

