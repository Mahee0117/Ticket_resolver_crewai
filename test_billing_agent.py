from crewai import Crew, Task
from supportcrew_ai.agents import billing_agent

task = Task(
    description=(
        "Customer asks: What is the status of order ORD101? "
        "Use the get_order_status tool to retrieve the actual order details. "
        "Report the status and expected delivery date. Do not guess."
    ),
    expected_output="Order status and expected delivery date",
    agent=billing_agent
)

crew = Crew(
    agents=[billing_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print("\nFINAL RESPONSE:")
print(result)