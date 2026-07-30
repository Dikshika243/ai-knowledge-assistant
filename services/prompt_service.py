from langchain_core.prompts import PromptTemplate


class PromptService:

    TEMPLATE = """
You are an AI assistant.

Use ONLY the provided context to answer the question.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    def __init__(self):
        self.prompt_template = PromptTemplate(
            template=self.TEMPLATE,
            input_variables=["context", "question"],
        )

    def build_prompt(
        self,
        question: str,
        context_documents: list[str]
    ) -> str:

        context = "\n\n".join(context_documents)

        return self.prompt_template.format(
            context=context,
            question=question,
        )