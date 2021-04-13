import asyncio
import aiohttp


urls = [
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg",
]


async def download(url):
    name = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as reponse:
            with open(name, mode='wb') as f:
                f.write(await reponse.content.read())
    print(name, 'Download complete!')


async def main():
    tasks = []
    for url in urls:
        tasks.append(download(url))

    await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
