from crewai import Crew

from supportcrew_ai.agents import (
    triage_agent,
    billing_agent,
    technical_agent,
    general_support_agent,
    account_agent,
    qa_agent
)

from supportcrew_ai.tasks import (
    create_triage_task,
    create_billing_task,
    create_technical_task,
    create_general_support_task,
    create_account_task,
    create_qa_task
)

from supportcrew_ai.tickets import tickets


# Maximum number of retries after QA rejection
MAX_RETRIES = 2


def run_triage(ticket):
    """
    Run the triage agent and classify the customer ticket.
    """

    triage_task = create_triage_task(
        ticket,
        triage_agent
    )

    triage_crew = Crew(
        agents=[triage_agent],
        tasks=[triage_task],
        verbose=False
    )

    return triage_crew.kickoff()


def run_specialist(
    category,
    ticket,
    previous_response=None,
    qa_feedback=None
):
    """
    Run the appropriate specialist agent.

    If QA rejected a previous response, the previous response
    and QA feedback are passed to the specialist so it can
    improve its answer.
    """

    if category == "Billing":

        agent = billing_agent

        task = create_billing_task(
            ticket,
            agent,
            previous_response,
            qa_feedback
        )

    elif category == "Technical":

        agent = technical_agent

        task = create_technical_task(
            ticket,
            agent,
            previous_response,
            qa_feedback
        )

    elif category == "General":

        agent = general_support_agent

        task = create_general_support_task(
            ticket,
            agent,
            previous_response,
            qa_feedback
        )

    elif category == "Account":

        agent = account_agent

        task = create_account_task(
            ticket,
            agent,
            previous_response,
            qa_feedback
        )

    else:
        raise ValueError(
            f"Unknown ticket category: {category}"
        )

    specialist_crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    return specialist_crew.kickoff()


def run_quality_check(ticket, specialist_response):
    """
    Run the QA agent to evaluate the specialist response.
    """

    qa_task = create_qa_task(
        ticket,
        specialist_response,
        qa_agent
    )

    qa_crew = Crew(
        agents=[qa_agent],
        tasks=[qa_task],
        verbose=False
    )

    return qa_crew.kickoff()


def main():

    print("\n======================================")
    print("      SUPPORTCREW AI - V2")
    print("   Multi-Agent Support + QA System")
    print("======================================")

    for index, ticket in enumerate(tickets, start=1):

        print("\n\n======================================")
        print(f"TICKET {index}")
        print("======================================")

        print("\nCustomer Ticket:")
        print(ticket)

        # ----------------------------------
        # STEP 1: TRIAGE
        # ----------------------------------

        print("\n--- Triage Stage ---")

        triage_result = run_triage(ticket)

        triage_data = triage_result.pydantic

        print("\nTriage Result:")
        print("Category:", triage_data.category)
        print("Priority:", triage_data.priority)
        print("Issue:", triage_data.issue)

        # ----------------------------------
        # STEP 2: SPECIALIST + QA LOOP
        # ----------------------------------

        previous_response = None
        qa_feedback = None

        for attempt in range(MAX_RETRIES + 1):

            print(
                f"\n--- Specialist Attempt {attempt + 1} ---"
            )

            # ------------------------------
            # SPECIALIST
            # ------------------------------

            specialist_result = run_specialist(
                triage_data.category,
                ticket,
                previous_response,
                qa_feedback
            )

            specialist_response = specialist_result.raw

            print("\nSpecialist Response:")
            print(specialist_response)

            # ------------------------------
            # QA
            # ------------------------------

            print("\n--- QA Stage ---")

            qa_result = run_quality_check(
                ticket,
                specialist_response
            )

            qa_data = qa_result.pydantic

            print("\nQA Result:")
            print("Approved:", qa_data.approved)
            print("Feedback:", qa_data.feedback)

            # ------------------------------
            # APPROVED
            # ------------------------------

            if qa_data.approved:

                print(
                    "\n✅ Response approved by QA."
                )

                print(
                    f"\n🎯 Final response accepted "
                    f"after {attempt + 1} attempt(s)."
                )

                break

            # ------------------------------
            # REJECTED
            # ------------------------------

            print(
                "\n❌ QA rejected the response."
            )

            previous_response = specialist_response
            qa_feedback = qa_data.feedback

            # ------------------------------
            # MAX RETRIES
            # ------------------------------

            if attempt == MAX_RETRIES:

                print(
                    "\n⚠️ Maximum retries reached."
                )

                print(
                    "The response could not pass QA."
                )

                break

            print(
                "\n🔄 Sending QA feedback back "
                "to the specialist agent..."
            )


if __name__ == "__main__":
    main()