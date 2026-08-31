from langchain_core.prompts import ChatPromptTemplate

report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Legal Report Generator.

Your job is to convert the analyst's findings into a professional legal report.

Structure:

1. Executive Summary
2. Contract Findings
3. Legal Risks
4. Compliance Assessment
5. Recommendations

Use professional formatting.

Do not invent facts.
"""
        ),
        (
            "human",
            """
Question:
{question}

Analysis Type:
{analysis_type}

Analysis:
{analysis}
"""
        ),
    ]
)