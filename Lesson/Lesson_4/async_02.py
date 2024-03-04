import asyncio


async def count():
    print('start')
    await asyncio.sleep(1)
    print('1 second has passed')
    await asyncio.sleep(2)
    print('2 second has passed')
    return 'ready'


async def main():
    result = await asyncio.gather(count(), count(), count())
    print(result)

asyncio.run(main())
