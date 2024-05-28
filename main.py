import aiohttp; import nest_asyncio; nest_asyncio.apply()
import aiofiles; import random; import asyncio
from urllib.parse import urljoin
from bs4 import BeautifulSoup
async def fetch_links(session: aiohttp.ClientSession, url: str, visited_urls: set = None) -> list[str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }
    async with session.get(url, headers=headers, allow_redirects=True) as response:
        if response.status == 200 or response.status == 404:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            return [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href') and link.get('href').startswith(('http://', 'https://'))]
        return []

async def main() -> None:
    urls = [
        'https://regex101.com/',
        'https://docs.python.org/3/this-url-will-404.html',
        'https://www.nytimes.com/guides/',
        'https://www.mediamatters.org/',
        'https://1.1.1.1/',
        'https://www.politico.com/tipsheets/morning-money',
        'https://www.bloomberg.com/markets/economics',
        'https://www.ietf.org/rfc/rfc2616.txt'
    ]
    async with aiohttp.ClientSession() as session, aiofiles.open('links.txt', 'w') as f:
        tasks = [asyncio.ensure_future(fetch_links(session, url)) for url in urls]
        for task in asyncio.as_completed(tasks):
            links = await task
            await f.write('\n'.join(links) + '\n')
            await asyncio.sleep(random.uniform(0.1, 0.3))
asyncio.run(main())
