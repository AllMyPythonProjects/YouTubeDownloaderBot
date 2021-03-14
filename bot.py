import config
import logging
from pytube.exceptions import RegexMatchError, VideoUnavailable
from pytube import YouTube
import os

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def sendVideo(message: types.Message):
    try:
        link = message.text
        yt = YouTube(link)
        file_name = yt.title + '.mp4'
        ys = yt.streams.get_highest_resolution()
        path = os.path.dirname(os.path.abspath(__file__)) + '/video/'
        ys.download(path, 'tmp')
        # print(f'\n\n{os.path.exists(path + file_name)}\n\n')
        file = open(path + 'tmp.mp4', 'rb')
        await bot.send_video(message.from_user.id, file)
        os.remove(path + 'tmp.mp4')
    except RegexMatchError as ex:
        await message.answer('Такого видео не существует :(')
    except VideoUnavailable as ex:
        await message.answer('Такого видео не существует :(')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
