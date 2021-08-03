import time
from selenium import webdriver
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = '1901407828:AAEnLtacN1E2_WzsrTbbIntKuPnhtMXE2FQ'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.reply("""
    Привет!
    Напиши /help для более подробной информации
    Чтобы скачать видео нужно:
    Переслать видео которое кинул бот
    С командой /dow
    Мой создатель Bohdan""")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.reply(
        'Для работы нужно написать текст для поиска и через пробел количество видео (по умолчанию количество видео равно 1')


@dp.message_handler(commands=['dow'])
async def send_photo(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'https://ru.savefrom.net/7/#url=' + msg['reply_to_message']['text'])


@dp.message_handler()
async def result(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Идёт поиск')
    text = msg.text.split(' ')
    if len(text) == 1:
        count = int(1)
    else:
        count = int(text[1])
    browser = webdriver.Firefox()
    browser.get(f'https://www.youtube.com/results?search_query={text[0]}')
    block = browser.find_element_by_class_name('style-scope ytd-item-section-renderer')
    all_video = block.find_elements_by_tag_name('ytd-video-renderer')
    if all_video:
        for video in all_video[:count]:
            await bot.send_message(msg.from_user.id, video.find_element_by_id('video-title').get_attribute('href'))
    else:
        await bot.send_message(msg.from_user.id, f"Видео с именем {text[0]} не найдено")
    browser.quit()


executor.start_polling(dp)
