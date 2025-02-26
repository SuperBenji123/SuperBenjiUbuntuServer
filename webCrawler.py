import asyncio
import sys
from crawl4ai import *

async def main(sentUrl):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=sentUrl,
        )
        print(result.model_dump_json)

if __name__ == "__main__":
    # Read URL from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 webCrawler.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    asyncio.run(main(url))