from config.openai_client import llm

from prompts.contract_analyst_prompt import contract_analyst_prompt


contract_analyst_chain = contract_analyst_prompt | llm


def contract_analyst_agent(
    question,
    analysis_type,
    contract_context,
    legal_references,
):

    response = contract_analyst_chain.invoke(
        {
            "question": question,
            "analysis_type": analysis_type,
            "contract_context": contract_context,
            "legal_references": legal_references,
        }
    )

    return response.content