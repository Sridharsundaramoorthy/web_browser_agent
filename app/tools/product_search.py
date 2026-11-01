import asyncio

from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()


search_tool = TavilySearch(
    max_results=5,
    topic="general",
)


async def search_website(website, product):

    query = f"site:{website} {product} price India buy"

    try:

        result = await asyncio.to_thread(
            search_tool.invoke,
            {"query": query},
        )

        return {
            "website": website,
            "results": result.get("results", []),
        }

    except Exception as error:

        print(f"[SEARCH ERROR] {website}: {error}")

        return {
            "website": website,
            "results": [],
            "error": str(error),
        }


async def search_all_websites(product):

    websites = [
        "amazon.in",
        "flipkart.com",
        "croma.com",
    ]

    tasks = [
        search_website(website, product)
        for website in websites
    ]

    results = await asyncio.gather(*tasks)

    return results