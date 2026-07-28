class PromptBuilder:

    @staticmethod
    def build_prompt(question: str, context_documents: list[str]) -> str:

        context = "\n\n".join(context_documents)

        return f"""
You are a helpful document assistant.

Your job is to answer the user's question using ONLY the information provided below.

Instructions:
- Carefully read the entire context before answering.
- Extract the answer directly from the context.
- If the answer exists, answer it naturally.
- Do NOT say "I couldn't find the answer" unless the information is completely missing.
- Do not invent information.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""