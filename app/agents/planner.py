from typing import Optional

from pydantic import BaseModel, Field

from app.llm import llm


class ProductRequirements(BaseModel):

    product: str = Field(
        description="Exact product name"
    )

    brand: Optional[str] = Field(
        default=None,
        description="Brand name"
    )

    budget: Optional[float] = Field(
        default=None,
        description="Maximum budget in INR, if specified"
    )

    specifications: list[str] = Field(
        default_factory=list,
        description="Storage, colour, size and other specifications"
    )

    condition: str = Field(default="new")

    country: str = Field(default="India")


structured_llm = llm.with_structured_output(ProductRequirements)


def planner_agent(state):

    question = state["user_question"]

    print("\n[PLANNER] Understanding user request...")
    print(f"[PLANNER] Question: {question}")

    requirements = structured_llm.invoke(
        f"""
        Extract shopping requirements from this request.

        User request: {question}

        Rules:
        - Identify the exact product.
        - Extract brand if specified.
        - Extract budget in INR if specified.
        - Extract technical specifications.
        - Include colour, storage, size and model variants.
        - Default country to India.
        - Default condition to new.
        - Do not invent missing requirements.
        - Keep budget as null if the user did not specify one.
        """
    )

    result = requirements.model_dump()

    print("\n[PLANNER] Extracted requirements:")
    print(result)

    return {
        **state,
        "product_requirements": result,
    }