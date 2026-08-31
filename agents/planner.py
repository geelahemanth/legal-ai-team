from urllib import response
from langchain_core.prompts import ChatPromptTemplate
from config.openai_client import llm
import json
from models.planner_output import PlannerOutput


planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Legal Workflow Planner.

For the user's question:

1. Identify the analysis type.
2. Generate a concise search query for retrieving relevant passages
   from the uploaded contract.
3. Decide whether external legal research is required.

Important:
- Always generate a non-empty search_query.
- search_query is used for contract retrieval.
- requires_research is only for deciding whether external legal research
  is needed.
- Set requires_research=false when the uploaded contract is sufficient.
- Set requires_research=true when the question requires external law,
  regulations, case law, or legal precedent.

Return only the structured output.
"""
    ),
    ("human", "{question}")
])

planner_chain = planner_prompt | llm.with_structured_output(PlannerOutput)

def planner_agent(question: str):

    response = planner_chain.invoke(
    {
        "question": question
    }
    )
    print(f"Planner Agent Response: {response}")
    return response.model_dump()