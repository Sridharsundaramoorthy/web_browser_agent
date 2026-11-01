from typing import Optional

from pydantic import BaseModel, Field

from app.llm import llm


class ComparedProduct(BaseModel):

    product_name: str = Field(
        description="Exact product name"
    )

    website: str = Field(
        description="Store website, such as amazon.in, flipkart.com or croma.com"
    )

    price: Optional[float] = Field(
        default=None,
        description="Product price in INR. Null if unavailable."
    )

    delivery_charge: Optional[float] = Field(
        default=None,
        description="Delivery charge in INR. Null if unavailable."
    )

    product_url: Optional[str] = Field(
        default=None,
        description="Original product URL from search results"
    )

    brand: Optional[str] = None

    specifications: list[str] = Field(
        default_factory=list
    )

    color: Optional[str] = None

    storage: Optional[str] = None

    price_verified: bool = Field(
        default=False,
        description=(
            "True only when the actual product price is explicitly "
            "supported by the supplied search result."
        )
    )


class ProductComparison(BaseModel):

    products: list[ComparedProduct] = Field(
        default_factory=list
    )


structured_llm = llm.with_structured_output(ProductComparison)


def comparison_agent(state):

    print("\n[COMPARISON] Comparing products...")

    search_results = state.get("search_results", [])

    requirements = state.get("product_requirements", {})

    if not search_results:

        print("[COMPARISON] No search results.")

        return {
            **state,
            "matched_products": [],
            "price_comparison": [],
            "status": "no_products_found",
        }

    comparison = structured_llm.invoke(
        f"""
        You are an e-commerce product comparison agent.

        USER REQUIREMENTS:
        {requirements}

        SEARCH RESULTS:
        {search_results}

        Instructions:

        1. Find products matching the requested product.
        2. Match brand, storage and colour wherever specified.
        3. Extract the actual price in Indian Rupees.
        4. Never invent prices.
        5. Never assume delivery is free.
        6. If delivery charge is unavailable, return null.
        7. Use the original URL from the search result.
        8. Never create fake product URLs.
        9. Exclude unrelated products.
        10. Mark price_verified true only if an actual price
            is explicitly present in the search result.
        11. If the price is missing, return null.
        12. Do not treat EMI amounts as the full product price.
        13. Do not treat a different storage or colour variant
            as an exact match.

        Return the matching products in structured format.
        """
    )

    products = [
        product.model_dump()
        for product in comparison.products
    ]

    print(
        f"[COMPARISON] Compared {len(products)} products."
    )

    for product in products:

        print("\n------------------------------")

        print("Product:", product["product_name"])
        print("Website:", product["website"])
        print("Price:", product["price"])
        print("Delivery:", product["delivery_charge"])
        print("Price supported by result:", product["price_verified"])

    return {
        **state,
        "matched_products": products,
        "price_comparison": products,
        "status": "comparison_completed",
    }