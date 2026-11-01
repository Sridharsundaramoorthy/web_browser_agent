from typing import TypedDict


class ShoppingState(TypedDict, total=False):

    # User request
    user_question: str

    # Parsed requirements
    product_requirements: dict

    # Search results
    search_results: list

    # Matching products
    matched_products: list

    # Price comparison
    price_comparison: list

    # Selected product
    selected_product: dict

    # User approval
    product_approved: bool

    # Workflow status
    status: str

    # Final response
    final_response: str