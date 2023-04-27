import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
import ssl

BASE_URL="https://globus-online.kg/catalog/ovoshchi_frukty_orekhi_zelen/ovoshchi/"
HEADERS = {"User-Agent":UserAgent().random}

async def main():
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
                print(f'TITLE:{" ".join(div)}   {" ".join(price)}   {short_price}')
                #Перец Испанский 380 сом 
if __name__ =='__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())