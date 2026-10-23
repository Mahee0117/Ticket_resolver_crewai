
from crewai.tools import tool

from supportcrew_ai.rag.knowledge_base import search_knowledge_base


@tool("search_support_knowledge")
def search_support_knowledge(query: str) -> str:
    """Search official project support documentation for relevant
    troubleshooting steps, account guidance, security guidance,
    refund policies, and order-delivery procedures.

    Use this tool before answering questions that may be covered
    by the support knowledge base. Base product-specific guidance
    on the retrieved documents. If no relevant information is found,
    say that the knowledge base does not contain enough information.
    """
    results = search_knowledge_base(query, top_k=3)

    if not results:
        return "No relevant support documentation was found."

    return "\n\n---\n\n".join(results)
