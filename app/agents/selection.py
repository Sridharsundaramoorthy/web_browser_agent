def selection_agent(state):

    print("\n[SELECTION] Selecting the best deal")

    products = state.get("price_comparison", [])

    requirements = state.get("product_requirements", {})

    budget = requirements.get("budget")

    eligible = []

    for product in products:

        price = product.get("price")

        delivery = product.get("delivery_charge")

        price_verified = product.get("price_verified", False)

        # Reject products without a supported price.
        if price is None or not price_verified:
            continue

        # Apply budget when specified.
        if budget is not None and price > budget:
            continue

        # Calculate total only when delivery is known.
        total = (
            price + delivery
            if delivery is not None
            else None
        )

        product["total_price"] = total

        eligible.append(product)

    if not eligible:

        print("[SELECTION] No verified products available.")

        return {
            **state,
            "selected_product": {},
            "status": "no_verified_deal",
            "final_response": (
                "Matching products were searched, but no product "
                "with a sufficiently supported price was found. "
                "Please verify the current price on the retailer's website."
            ),
        }

    # Prefer products with a known total price.
    eligible.sort(
        key=lambda item: (
            item["total_price"] is None,
            item["total_price"]
            if item["total_price"] is not None
            else item["price"],
        )
    )

    selected = eligible[0]

    delivery_text = (
        f"₹{selected['delivery_charge']}"
        if selected["delivery_charge"] is not None
        else "Not confirmed"
    )

    total_text = (
        f"₹{selected['total_price']}"
        if selected["total_price"] is not None
        else "Not confirmed"
    )

    print("[SELECTION] Best matching product selected.")

    return {
        **state,
        "selected_product": selected,
        "status": "awaiting_approval",
        "final_response": (
            f"Recommended product: {selected['product_name']}\n"
            f"Website: {selected['website']}\n"
            f"Price: ₹{selected['price']}\n"
            f"Delivery charge: {delivery_text}\n"
            f"Total price: {total_text}\n"
            f"Product URL: {selected['product_url']}"
        ),
    }