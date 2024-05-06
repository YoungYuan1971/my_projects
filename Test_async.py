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
    # 创建异步请求上下文
    async with session.get(url) as reponse:
        # 创建异步文件读写上下文
        async with aiofiles.open(f'00{num+1}.png', mode='wb') as f:
            # 写入文件
            await f.write(await reponse.read())
            # 返回执行状态
            return f"{url}...Download completed!"


async def main():
    # 创建异步会话上下文
    async with aiohttp.ClientSession() as session:
        # 创建任务列表
        tasks = []
        for url_index, url in enumerate(urls):
            tasks.append(asyncio.create_task(
                download(url, url_index, session)))

        # 获取返回数据
        for t in asyncio.as_completed(tasks):
            print(await t)

        # 等待所有任务完成
        await asyncio.wait(tasks)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
