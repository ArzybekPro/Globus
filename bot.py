import asyncio,aiohttp,ssl,os, logging, requests

from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor


load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


BASE_URL="https://globus-online.kg/catalog/ovoshchi_frukty_orekhi_zelen/ovoshchi/"
HEADERS = {"User-Agent":UserAgent().random}


@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hellow World")

@dp.message_handler(commands = 'vegatebles')
async def main(message:types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS, ssl=False) as response:
            r = await response.content.read()
            soup = BS(r,'html.parser')
            items = soup.find_all('div',{'class':'js-element__shadow'})
            shortener = Shortener(timeout=5)
            for item in items:
                title = item.find('a')
                link = title.get('href')
                div = item.find('div',{'class':'list-showcase__name'}).text.split()
                price = item.find('span',{'c-prices__value'}).text.split()
                short_price = shortener.tinyurl.short(f'https://globus-online.kg{link}')
                await message.answer(f'TITLE:{" ".join(div)}   {" ".join(price)}   {short_price}')

                
if __name__ =='__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop.run_until_complete(main())
    executor.start_polling(dp)