import json
import time
import asyncio

from news_collector import fetch_articles
async def gather(limit=2):
    tasks = []
    for source, (
        data_path,
        url,
        title_selector,
        paragraphs_selector,
        link_selector,
    ) in NEWS_DICT.items():
        task = fetch_articles(
            source,
            data_path,
            url,
            title_selector=title_selector,
            paragraphs_selector=paragraphs_selector,
            link_selector=link_selector,
        )
        tasks.append(task)

    start = time.time()
    await asyncio.gather(*tasks)
    end = time.time()

    print(f"Total time to collect news: {end - start}s \n")
    
    # Writing data to JSON file
    data = {
        'elabc': elabc,
        'elconfidencial': elconfidencial,
        'elpais': pais,
        'lavanguardia': lavanguardia,
        'elespanol': espanol
    }
    
    with open('data/raw_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    end = time.time()
    print(f"\n  - Total time to collect: {end - start:.2f}s ")
    print(f"  - Total number of articles fetched: {sum(len(d) for d in data.values() if d is not None)} \n")

if __name__ == "__main__":
    asyncio.run(gather(2))