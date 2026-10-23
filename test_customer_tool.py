
from crewai import Crew, Task
from supportcrew_ai.agents import account_agent

task = Task(
    description=(
        "A customer has provided customer ID C101. "
        "Use the get_customer tool to look up their record. "
        "Report the customer's name and account status using the returned data. "
        "Do not guess the result."
    ),
    expected_output=(
        "The customer's name and account status, based on the tool result."
    ),
    agent=account_agent
)

crew = Crew(
    agents=[account_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

print("\n--- TOOL TEST RESULT ---")
print(result)
