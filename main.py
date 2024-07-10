from gatherer.news_collector import gather
from summarizer.summarizer_ollama import summarize
import time
import asyncio

async def main():
    await gather(5)
    summarize()
    
if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print("Time elapsed during gathering and summarize: ", end - start)
    
