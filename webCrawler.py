import asyncio
from crawl4ai import *

async def main(sentUrl):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=sentUrl,
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
