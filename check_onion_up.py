import aiohttp
import asyncio
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector
import re

async def check_onion_site(session, url):
    try:
        if not url.startswith('http://'):
            url = 'http://' + url
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                print(f"UP: {url}")
                return url
            else:
                pass
    except Exception as e:
        pass
    return None

async def check_onion_sites(file_path):
    tor_proxy = "socks5://127.0.0.1:9050"
    connector = ProxyConnector.from_url(tor_proxy)
    
    async with ClientSession(connector=connector) as session:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if re.search(r'\.onion$', line.strip())]
        
        tasks = [check_onion_site(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return [url for url in results if url is not None]

async def main():
    file_path = "onion_list.txt"
    alive_onion_sites = await check_onion_sites(file_path)
    
    print("\nONION SITES UP:")
    for site in alive_onion_sites:
        print(site)

if __name__ == "__main__":
    asyncio.run(main())
