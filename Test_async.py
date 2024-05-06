import asyncio
import aiohttp
import aiofiles

urls = [
    "https://images.pexels.com/photos/22626143/pexels-photo-22626143.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/21751135/pexels-photo-21751135.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/20604045/pexels-photo-20604045.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/21529784/pexels-photo-21529784.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/20922644/pexels-photo-20922644.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/20545539/pexels-photo-20545539.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
]


# 异步协程获取数据：response.read() 获取二进制字节流；response.text() 获取字符串；response.json() 获取JSON格式数据
async def download(url, num, session):
    async with session.get(url) as reponse:
        async with aiofiles.open(f'00{num+1}.png', mode='wb') as f:
            await f.write(await reponse.read())
            return f"{url}...Download completed!"


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url_index, url in enumerate(urls):
            tasks.append(asyncio.create_task(
                download(url, url_index, session)))

        for t in asyncio.as_completed(tasks):
            print(await t)

        await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
