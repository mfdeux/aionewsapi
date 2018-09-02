import asyncio

from aionewsapi import NewsAPI

news_api = NewsAPI()


async def sources():
    return await news_api.sources()


async def many():
    sources = await news_api.sources()
    fetch_tasks = []
    for source in sources:
        fetch_tasks.append(
            asyncio.ensure_future(
                news_api.latest_articles(
                    source.get('id'),
                    source.get('sorts_available')[0])))
    for index, task in enumerate(asyncio.as_completed(fetch_tasks)):
        result = await task
        print('FETCH Task ret {}: {}'.format(index, result))


async def latest_articles():
    return await news_api.latest_articles('the-washington-post', 'top')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(latest_articles())
    print(loop.run_until_complete(task))
