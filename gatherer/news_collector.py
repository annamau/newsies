import json
import time
import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from constants import NEWS_DICT

ua = UserAgent()


async def fetch_html(session, link):
    try:
        async with session.get(
            link, headers={"User-Agent": str(ua.random)}
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error fetching {link}, status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Error fetching {link}: {e}")


async def extract_article(html, link, title_selector, paragraphs_selector):
    try:
        soup = BeautifulSoup(html, "lxml")
        title = soup.select_one(title_selector).getText()
        paragraphs = soup.select(paragraphs_selector)
        text = "\n".join([paragraph.getText() for paragraph in paragraphs])
        return {
            "title": re.sub(r"\s+", " ", title.encode().decode("unicode_escape")).strip(),
            "text": re.sub(r"\s+", " ", text.encode().decode("unicode_escape")).strip(),
            "link": link,
        }
    except AttributeError as e:
        print(f"Error extracting article from {link}: {e}")


async def fetch_articles(
    source,
    data_path,
    url,
    limit=30,
    title_selector=None,
    paragraphs_selector=None,
    link_selector=None,
):
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, url)
        if not html:
            return

        soup = BeautifulSoup(html, "lxml")
        articles_raw = soup.find_all("article", limit=limit)
        article_links = []
        for article in articles_raw:
            if article.find(link_selector):
                link = article.find(link_selector).get("href")
                if not link:
                    continue
                elif link.startswith("http"):
                    article_links.append(link)
                else:
                    article_links.append(url + link)

        tasks = [fetch_html(session, link) for link in article_links]
        htmls = await asyncio.gather(*tasks)

        tasks = [
            extract_article(html, link, title_selector, paragraphs_selector)
            for html, link in zip(htmls, article_links)
        ]
        results = await asyncio.gather(*tasks)

    data = [result for result in results if result is not None]

    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nAll articles found from {source} and extracted!")
    print(f"Total number of articles: {len(data)}")


async def main():
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


if __name__ == "__main__":
    asyncio.run(main())
