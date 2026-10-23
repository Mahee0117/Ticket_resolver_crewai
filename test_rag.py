
from supportcrew_ai.rag.knowledge_base import (
    build_knowledge_base,
    search_knowledge_base,
)

build_knowledge_base()

questions = [
    "The customer never received a password reset email.",
    "The app crashes when a PDF is uploaded.",
    "Where is order ORD101 and when will it arrive?",
    "A customer reports transactions they did not make.",
]

for question in questions:
    print(f"\nQUESTION: {question}")
    print("-" * 60)

    results = search_knowledge_base(question, top_k=2)

    for index, result in enumerate(results, start=1):
        print(f"\nRESULT {index}:\n{result}")
