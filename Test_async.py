import asyncio
import aiohttp
import aiofiles

urls = [
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/a2c58d6d726fb7ef29390becac5d8643.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/d7de3f9faf1e0ecdea27b73139fc8d3a.jpg",
    "http://kr.shanghai-jiuxin.com/file/2021/0326/0311c15cb53c16319db5f0a7ceb68642.jpg",
]


async def download(url):
    name = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as reponse:
            async with aiofiles.open(name, mode='wb') as f:
                await f.write(await reponse.content.read())
                print(name, 'Download complete!')


async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))

    await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
