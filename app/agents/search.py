import asyncio

from app.tools.product_search import search_all_websites


def product_search_agent(state):

    print("\n[SEARCH] Searching e-commerce websites")

    requirements = state["product_requirements"]

    product = requirements["product"]

    brand = requirements.get("brand") or ""

    specifications = " ".join(
        requirements.get("specifications", [])
    )

    search_query = (
        f"{brand} {product} {specifications}"
    ).strip()

    print(f"[SEARCH] Query: {search_query}")

    results = asyncio.run(
        search_all_websites(search_query)
    )

    all_results = []

    for website_result in results:

        website = website_result["website"]

        for item in website_result.get("results", []):

            all_results.append({
                "website": website,
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
            })

    print(
        f"[SEARCH] Found {len(all_results)} search results"
    )

    return {
        **state,
        "search_results": all_results,
        "status": "search_completed",
    }