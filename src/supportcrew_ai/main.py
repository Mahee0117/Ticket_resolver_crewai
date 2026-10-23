
from crewai import Crew

from supportcrew_ai.rag.knowledge_base import (
    ensure_knowledge_base,
    search_knowledge_base,
)
from supportcrew_ai.agents import (
    triage_agent,
    billing_agent,
    technical_agent,
    general_support_agent,
    account_agent,
    qa_agent,
)
from supportcrew_ai.tasks import (
    create_triage_task,
    create_billing_task,
    create_technical_task,
    create_general_support_task,
    create_account_task,
    create_qa_task,
)
from supportcrew_ai.tickets import tickets


# Maximum retries after QA rejection.
# One initial attempt + two retries = three maximum attempts.
MAX_RETRIES = 2


def run_triage(ticket):
    """Classify a customer support ticket."""

    triage_task = create_triage_task(ticket, triage_agent)

    triage_crew = Crew(
        agents=[triage_agent],
        tasks=[triage_task],
        verbose=False,
    )

    return triage_crew.kickoff()


def run_specialist(
    category,
    ticket,
    previous_response=None,
    qa_feedback=None,
):
    """Run the specialist selected by the triage category."""

    if category == "Billing":
        agent = billing_agent
        task = create_billing_task(
            ticket, agent, previous_response, qa_feedback
        )

    elif category == "Technical":
        agent = technical_agent
        task = create_technical_task(
            ticket, agent, previous_response, qa_feedback
        )

    elif category == "General":
        agent = general_support_agent
        task = create_general_support_task(
            ticket, agent, previous_response, qa_feedback
        )

    elif category == "Account":
        agent = account_agent
        task = create_account_task(
            ticket, agent, previous_response, qa_feedback
        )

    else:
        raise ValueError(f"Unknown ticket category: {category}")

    specialist_crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    return specialist_crew.kickoff()


def run_quality_check(
    ticket,
    specialist_response,
    retrieved_evidence="",
):
    """Evaluate a specialist response using QA."""

    qa_task = create_qa_task(
        ticket,
        specialist_response,
        qa_agent,
        retrieved_evidence,
    )

    qa_crew = Crew(
        agents=[qa_agent],
        tasks=[qa_task],
        verbose=False,
    )

    return qa_crew.kickoff()


def process_ticket(ticket):
    """
    Process one user-submitted ticket for the Streamlit UI.

    Returns triage, specialist response, QA status, retry count,
    and retrieved evidence.
    """

    if not isinstance(ticket, str) or not ticket.strip():
        raise ValueError("Please enter a support ticket.")

    ticket = ticket.strip()

    # STEP 1: TRIAGE
    triage_result = run_triage(ticket)
    triage_data = triage_result.pydantic

    # STEP 2: RETRIEVE EVIDENCE FOR QA
    retrieved_evidence = ""

    if triage_data.category == "Technical":
        evidence_chunks = search_knowledge_base(
            ticket,
            top_k=3,
        )
        retrieved_evidence = "\n\n---\n\n".join(evidence_chunks)

    # STEP 3: SPECIALIST + QA RETRY LOOP
    previous_response = None
    qa_feedback = None
    specialist_response = ""
    qa_data = None
    approved = False
    attempts = 0

    for attempt in range(MAX_RETRIES + 1):
        attempts = attempt + 1

        specialist_result = run_specialist(
            triage_data.category,
            ticket,
            previous_response,
            qa_feedback,
        )

        specialist_response = specialist_result.raw

        qa_result = run_quality_check(
            ticket,
            specialist_response,
            retrieved_evidence,
        )

        qa_data = qa_result.pydantic

        if qa_data.approved:
            approved = True
            break

        # Give the specialist another chance using QA feedback.
        previous_response = specialist_response
        qa_feedback = qa_data.feedback

    # STEP 4: RETURN RESULTS TO STREAMLIT
    return {
        "category": triage_data.category,
        "priority": triage_data.priority,
        "issue": triage_data.issue,
        "response": specialist_response,
        "qa_approved": approved,
        "qa_feedback": qa_data.feedback,
        "attempts": attempts,
        "evidence": retrieved_evidence,
    }


def main():
    """Run the original command-line workflow on predefined tickets."""

    print("\n======================================")
    print("      SUPPORTCREW AI - V3.0")
    print("   Multi-Agent Support + QA + RAG")
    print("======================================")

    for index, ticket in enumerate(tickets, start=1):
        print("\n\n======================================")
        print(f"TICKET {index}")
        print("======================================")

        print("\nCustomer Ticket:")
        print(ticket)

        print("\n--- Triage Stage ---")

        triage_result = run_triage(ticket)
        triage_data = triage_result.pydantic

        print("\nTriage Result:")
        print("Category:", triage_data.category)
        print("Priority:", triage_data.priority)
        print("Issue:", triage_data.issue)

        retrieved_evidence = ""

        if triage_data.category == "Technical":
            evidence_chunks = search_knowledge_base(
                ticket,
                top_k=3,
            )
            retrieved_evidence = "\n\n---\n\n".join(evidence_chunks)

            print("\n--- Evidence Retrieved for QA ---")
            print(
                retrieved_evidence
                if retrieved_evidence
                else "No relevant support evidence found."
            )

        previous_response = None
        qa_feedback = None
        approved = False

        for attempt in range(MAX_RETRIES + 1):
            print(f"\n--- Specialist Attempt {attempt + 1} ---")

            specialist_result = run_specialist(
                triage_data.category,
                ticket,
                previous_response,
                qa_feedback,
            )

            specialist_response = specialist_result.raw

            print("\nSpecialist Response:")
            print(specialist_response)

            print("\n--- QA Stage ---")

            qa_result = run_quality_check(
                ticket,
                specialist_response,
                retrieved_evidence,
            )

            qa_data = qa_result.pydantic

            print("\nQA Result:")
            print("Approved:", qa_data.approved)
            print("Feedback:", qa_data.feedback)

            if qa_data.approved:
                approved = True
                print("\nResponse approved by QA.")
                print(
                    f"Final response accepted after "
                    f"{attempt + 1} attempt(s)."
                )
                break

            print("\nQA rejected the response.")

            previous_response = specialist_response
            qa_feedback = qa_data.feedback

            if attempt < MAX_RETRIES:
                print("Sending QA feedback back to the specialist...")
            else:
                print("Maximum retries reached.")

        if not approved:
            print(
                "\nUNAPPROVED: No response passed QA. "
                "Human review is required."
            )


if __name__ == "__main__":
    ensure_knowledge_base()
    main()
