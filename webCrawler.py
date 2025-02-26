import asyncio
import sys
print("1")
from crawl4ai import *
print("2")

async def main(sentUrl):
    print("3")
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=sentUrl,
        )
        print(result.markdown)

if __name__ == "__main__":
    # Read URL from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 webCrawler.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    asyncio.run(main(url))