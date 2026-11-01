import uuid

from app.graph.shopping_graph import shopping_graph


def run_shopping_agent():

    print("\n================================")
    print("      AI SHOPPING ASSISTANT")
    print("================================")

    user_request = input(
        "\nWhat product do you want to buy? "
    ).strip()

    if not user_request:
        print("Please enter a product request.")
        return

    thread_id = str(uuid.uuid4())

    initial_state = {
        "user_question": user_request
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        result = shopping_graph.invoke(
            initial_state,
            config=config
        )

        print("\n================================")
        print("         SHOPPING RESULTS")
        print("================================")

        print(
            result.get(
                "final_response",
                "No final response was generated."
            )
        )

        print("\nWorkflow status:", result.get("status"))

        if result.get("matched_products"):

            print("\n===== MATCHED PRODUCTS =====")

            for index, product in enumerate(
                result["matched_products"],
                start=1
            ):

                print(f"\nProduct {index}")

                print("Name:", product.get("product_name"))
                print("Website:", product.get("website"))
                print("Price:", product.get("price"))
                print("URL:", product.get("product_url"))

        print("\nWorkflow ID:", thread_id)

    except Exception as error:

        print("\n[WORKFLOW ERROR]")
        print(error)


if __name__ == "__main__":

    run_shopping_agent()