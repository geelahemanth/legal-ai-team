from langgraph.graph import StateGraph, START, END
from graph.state import LegalState
from graph.nodes import (planner_node, research_node, retriever_node, contract_analyst_node,report_node)

def should_research(state):

    if state["requires_research"]:
        return "research"

    return "contract_analyst"


def build_graph():
    """ Build and compile the LangGraph workflow"""

    #create a grpah
    builder = StateGraph(LegalState)

    #Register nodes
    builder.add_node("planner", planner_node)
    builder.add_node("retriever", retriever_node)
    builder.add_node("research", research_node)
    builder.add_node("contract_analyst", contract_analyst_node)
    builder.add_node("report", report_node)


    #Define workflow
    builder.add_edge(START, "planner")

    builder.add_edge("planner", "retriever")
    builder.add_conditional_edges(
        "retriever", 
        should_research,
        {
            "research": "research",
            "contract_analyst": "contract_analyst"
        }
    )
    
    builder.add_edge("research", "contract_analyst")
    builder.add_edge("contract_analyst", "report")
    builder.add_edge("report", END)

    #graph compile
    graph = builder.compile()

    return graph



