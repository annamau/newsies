import json, time, aiohttp, asyncio, requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from constants import  CONFIDENCIAL_DATA_PATH, CONFIDENCIAL_URL

ua = UserAgent()

async def fetch_article(session, link):
    try:
        async with session.get(link, headers={'User-Agent':str(ua.random)}) as response:
            if response.status == 200:
                html = await response.text()
                soup = bs(html, "lxml")
                paragrafs = soup.find("main").find(id="news-body-cc").find_all("p")
                title = soup.find("title").getText()
                return {
                    "title": title,
                    "text": "\n".join([paragraf.getText() for paragraf in paragrafs]).strip(),
                    "link": link
                }
            else:
                print(f"Error fetching {link}, status code: {response.status}")
    except AttributeError as e:
        print(f"Error found at link {link}, error: {e}")
        
async def confidencial(limit=30):
    async with aiohttp.ClientSession() as session:
        html = requests.get(CONFIDENCIAL_URL, headers={'User-Agent':str(ua.random)})
        soup = bs(html.content, "lxml")
        articles_raw = soup.find_all("article", limit=limit)
        article_links = [article_raw.find("a")["href"] for article_raw in articles_raw if article_raw.find("a")]

        tasks = []
        for link in article_links:
            task = asyncio.create_task(fetch_article(session, link))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

    data = [result for result in results if result is not None]

    with open(CONFIDENCIAL_DATA_PATH, "w") as f:
        json.dump(data, f)

    print("\n All articles found from ELCONFIDENCIAL and extracted! \n")
    print(f"  - Total number of articles: {len(data)}")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(confidencial())
    end = time.time()
    print(f"  - Total time to collect from Confidencial: {end - start}s \n")