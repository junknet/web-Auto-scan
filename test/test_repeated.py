from asyncio.tasks import FIRST_EXCEPTION
import queue
import time
import asyncio
from asyncio.events import AbstractEventLoop

from queue import Queue
from threading import Thread


async def work(que: Queue):
    while True:
        data = que.get(timeout=1/5000)
        print(data)


async def async_run(loop: AbstractEventLoop, que: Queue):
    tasks = [loop.create_task(work(que)) for t in range(3)]
    await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)


def producer(que: Queue):
    for i in range(100):
        que.put(i)


def consumer(que: Queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_run(loop, que))
    loop.close()
    print("spend time  {}" .format(time.time()-start_time))


start_time = time.time()


que = Queue(maxsize=100,)
t1 = Thread(target=producer, args=(que,))
t2 = Thread(target=consumer, args=(que,))
t1.start()
t2.start()
