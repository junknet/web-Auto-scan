import asyncio
from asyncio import tasks
import queue
import re
import time
from asyncio.events import AbstractEventLoop, set_event_loop
from asyncio.tasks import FIRST_EXCEPTION
from queue import Queue
from threading import Thread
import aiohttp
from aiohttp.client import ClientSession
from scan.parse_request import RequestParse
from scan.plugin.generator import attack_request_generator


"""
构造出生产者消费者模型
分裂成2个线程
消费者线程使用协程做高并发
默认使用5000束协程 (执行器调度可能带来大开销 待测试)
2021.3.16 发包峰值为 1MB/s  4k包/1s
2021.3.17 测试结果 单线程开100个协程为最佳实践
2021.3.18 功能解耦
"""

# async def do_work(que: Queue):
#     async with aiohttp.ClientSession() as session:
#         while True:
#             try:
#                 (method, url, headers, data) = que.get(timeout=1)
#                 async with session.post(url=url, data=data, headers=headers) as response:
#                     qwe = await response.json()
#                     print(qwe)
#             except Exception as e:
#                 raise e
#                 return


# async def async_run(loop: AbstractEventLoop, que: Queue):
#     tasks = [loop.create_task(do_work(que)) for _ in range(2)]
#     await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)


async def get_response(session: ClientSession, url, headers, data):
    async with session.post(url=url, headers=headers, data=data) as response:
        return await response.json()


async def print_someting(string):
    global count
    global Debug
    count += 1
    if Debug:
        print(string, "send {} package".format(count))


async def post_data(que: Queue):
    while True:
        try:
            (method, url, headers, data) = que.get(timeout=1/100)
        except Exception as e:
            return
        async with aiohttp.ClientSession() as session:
            try:
                response = await get_response(session=session, url=url, headers=headers, data=data)
            except Exception as e:
                raise e
                return
            await print_someting(response)


def producer(que: Queue):
    parsed_request = RequestParse("../request_log/25-request.txt")
    attack_request_generator(parsed_request, que, Debug)


def consumer(que: Queue):
    start_time = time.time()
    global count
    count = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.ensure_future(post_data(que))for _ in range(100)]
    future = asyncio.gather(*tasks)
    loop.run_until_complete(future)
    print("spend time  {}" .format(time.time()-start_time))


def main():
    global Debug
    Debug = True
    que = Queue()
    producer_thread = Thread(target=producer, args=(que,))
    consumer_thread = Thread(target=consumer, args=(que,))
    producer_thread.start()
    consumer_thread.start()
