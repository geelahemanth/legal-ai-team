from config.openai_client import llm
from prompts.report_generator_prompt import report_prompt

report_chain = report_prompt | llm


def report_generator_agent(
    question,
    analysis_type,
    analysis,
):
    for chunk in report_chain.stream(
        
        {
            "question": question,
            "analysis_type": analysis_type,
            "analysis": analysis,
        }
    ):
        yield chunk.content