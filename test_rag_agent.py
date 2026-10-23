
from crewai import Crew, Task

from supportcrew_ai.agents import technical_agent


def main():
    task = Task(
        description=(
            "A customer says the application crashes whenever they "
            "upload a PDF.\n\n"
            "Instructions:\n"
            "1. First, call the search_support_knowledge tool with a "
            "query about PDF upload crashes.\n"
            "2. Read the retrieved documentation carefully.\n"
            "3. Answer using only troubleshooting steps supported by "
            "the returned documentation.\n"
            "4. Ask which browser or application version the customer "
            "is using.\n"
            "5. Ask whether the issue also occurs with other PDF files.\n"
            "6. Ask for the PDF file size and any error message.\n"
            "7. Do not invent a root cause or suggest unrelated fixes.\n"
            "8. If the issue persists, recommend escalation to "
            "technical support.\n"
            "9. If the knowledge base does not contain enough "
            "information, clearly say so."
        ),
        expected_output=(
            "A concise customer-facing response based on retrieved "
            "support documentation. It should request the relevant "
            "diagnostic details, avoid unsupported troubleshooting "
            "advice, and recommend escalation if the issue persists."
        ),
        agent=technical_agent,
    )

    crew = Crew(
        agents=[technical_agent],
        tasks=[task],
        verbose=True,
    )

    print("\n" + "=" * 60)
    print("SUPPORTCREW AI - RAG AGENT TEST")
    print("=" * 60)

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
