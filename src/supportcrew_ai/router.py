from crewai import Crew

from supportcrew_ai.agents import (
    Billing_agent,
    Technical_agent,
    General_support_agent,
    Account_agent
)

from supportcrew_ai.tasks import (
    create_billing_task,
    create_technical_task,
    create_general_support_task,
    create_account_task
)


def route_ticket(category, ticket):

    # ========================================================
    # BILLING
    # ========================================================

    if category == "Billing":

        billing_task = create_billing_task(
            ticket,
            Billing_agent
        )

        specialist_crew = Crew(
            agents=[Billing_agent],
            tasks=[billing_task],
            verbose=False
        )

        return specialist_crew.kickoff()


    # ========================================================
    # TECHNICAL
    # ========================================================

    elif category == "Technical":

        technical_task = create_technical_task(
            ticket,
            Technical_agent
        )

        specialist_crew = Crew(
            agents=[Technical_agent],
            tasks=[technical_task],
            verbose=False
        )

        return specialist_crew.kickoff()


    # ========================================================
    # ACCOUNT
    # ========================================================

    elif category == "Account":

        account_task = create_account_task(
            ticket,
            Account_agent
        )

        specialist_crew = Crew(
            agents=[Account_agent],
            tasks=[account_task],
            verbose=False
        )

        return specialist_crew.kickoff()


    # ========================================================
    # GENERAL
    # ========================================================

    elif category == "General":

        general_support_task = create_general_support_task(
            ticket,
            General_support_agent
        )

        specialist_crew = Crew(
            agents=[General_support_agent],
            tasks=[general_support_task],
            verbose=False
        )

        return specialist_crew.kickoff()


    # ========================================================
    # UNKNOWN CATEGORY
    # ========================================================

    else:

        raise ValueError(
            f"Unknown ticket category: {category}"
        )