import warnings

warnings.filterwarnings("ignore")

from crewai import Crew

from supportcrew_ai.agents import triage_agent

from supportcrew_ai.tasks import create_triage_task

from supportcrew_ai.tickets import tickets

from supportcrew_ai.router import route_ticket


# ============================================================
# PROCESS TICKETS
# ============================================================

for ticket in tickets:

    # ========================================================
    # 1. CREATE TRIAGE TASK
    # ========================================================

    triage_task = create_triage_task(
        ticket,
        triage_agent
    )


    # ========================================================
    # 2. RUN TRIAGE
    # ========================================================

    triage_crew = Crew(
        agents=[triage_agent],
        tasks=[triage_task],
        verbose=False
    )

    triage_result = triage_crew.kickoff()


    # ========================================================
    # 3. GET STRUCTURED TRIAGE RESULT
    # ========================================================

    triage_data = triage_result.pydantic


    print("\n")
    print("========================================")
    print("TRIAGE RESULT")
    print("========================================")

    print("Category :", triage_data.category)
    print("Priority :", triage_data.priority)
    print("Issue    :", triage_data.issue)


    # ========================================================
    # 4. ROUTE TO SPECIALIST
    # ========================================================

    specialist_result = route_ticket(
        triage_data.category,
        ticket
    )


    # ========================================================
    # 5. DISPLAY SPECIALIST RESULT
    # ========================================================

    print("\n========================================")
    print("SPECIALIST RESULT")
    print("========================================")

    print(specialist_result)