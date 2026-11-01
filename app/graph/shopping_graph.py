from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.state import ShoppingState

from app.agents.planner import planner_agent
from app.agents.search import product_search_agent
from app.agents.comparison import comparison_agent
from app.agents.selection import selection_agent


def build_shopping_graph():

    builder = StateGraph(ShoppingState)

    # Register agents
    builder.add_node("planner", planner_agent)

    builder.add_node("search", product_search_agent)

    builder.add_node("comparison", comparison_agent)

    builder.add_node("selection", selection_agent)

    # Workflow sequence
    builder.add_edge(START, "planner")

    builder.add_edge("planner", "search")

    builder.add_edge("search", "comparison")

    builder.add_edge("comparison", "selection")

    builder.add_edge("selection", END)

    # Development checkpoint storage
    checkpointer = InMemorySaver()

    graph = builder.compile(
        checkpointer=checkpointer
    )

    return graph


shopping_graph = build_shopping_graph()