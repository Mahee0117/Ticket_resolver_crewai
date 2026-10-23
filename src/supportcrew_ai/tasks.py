
from crewai import Task

from supportcrew_ai.models import TriageResult, QAResult


# ============================================================
# TRIAGE TASK
# ============================================================

def create_triage_task(ticket, agent):
    return Task(
        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. Category — choose exactly one:
           Billing, Account, Technical, General

        2. Priority — choose exactly one:
           Low, Medium, High, Urgent

        3. Issue — provide a short description of the customer's problem.
        """,
        expected_output="""
        A structured triage result containing:
        - category
        - priority
        - issue
        """,
        output_pydantic=TriageResult,
        agent=agent,
    )


# ============================================================
# BILLING TASK
# ============================================================

def create_billing_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None,
):
    feedback_section = ""

    if previous_response and qa_feedback:
        feedback_section = f"""
        PREVIOUS RESPONSE:
        {previous_response}

        QA FEEDBACK:
        {qa_feedback}

        Revise the previous response to address every QA issue.
        Do not repeat unsupported claims.
        """

    return Task(
        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:
        1. What is the billing problem?
        2. What should the customer do next?
        3. Provide a clear, customer-friendly resolution.

        ORDER LOOKUP RULES:
        - If the ticket asks about an order and provides an order ID,
          use the get_order_status tool.
        - Base order-specific statements on the tool result.
        - If the order is not found, clearly say so.
        - Never invent order status or delivery dates.

        {feedback_section}
        """,
        expected_output="""
        Billing Issue:
        Resolution:
        Next Step:
        """,
        agent=agent,
    )


# ============================================================
# TECHNICAL TASK
# ============================================================

def create_technical_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None,
):
    feedback_section = ""

    if previous_response and qa_feedback:
        feedback_section = f"""
        PREVIOUS RESPONSE:
        {previous_response}

        QA FEEDBACK:
        {qa_feedback}

        Revise the previous response to address every QA issue.
        Remove unsupported claims rather than merely rewording them.
        """

    return Task(
        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        MANDATORY KNOWLEDGE BASE RULES:

        1. Call search_support_knowledge before drafting the response.
        2. Use retrieved documentation as the source of truth for
           product-specific troubleshooting.
        3. Recommend only troubleshooting steps supported by the
           retrieved documentation.
        4. Do not invent root causes, product behavior, software updates,
           driver fixes, file-size limits, or company policies.
        5. If the root cause is unknown, explicitly state:
           "Cause not yet determined."
        6. Ask focused diagnostic questions when more information is needed.
        7. Recommend escalation when documented steps are insufficient.
        8. If the knowledge base lacks sufficient information, acknowledge
           that limitation instead of inventing a solution.

        RESPONSE REQUIREMENTS:
        - Explain the reported technical problem.
        - State only evidence-supported causes.
        - Provide documented troubleshooting steps only.
        - Ask relevant diagnostic questions when necessary.
        - Recommend escalation when appropriate.
        - Keep the response concise and professional.

        {feedback_section}
        """,
        expected_output="""
        Technical Problem:
        Evidence-Based Cause:
        Troubleshooting:
        Information Needed:
        Resolution or Escalation:
        """,
        agent=agent,
    )


# ============================================================
# GENERAL SUPPORT TASK
# ============================================================

def create_general_support_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None,
):
    feedback_section = ""

    if previous_response and qa_feedback:
        feedback_section = f"""
        PREVIOUS RESPONSE:
        {previous_response}

        QA FEEDBACK:
        {qa_feedback}

        Improve the previous response based on the QA feedback.
        """

    return Task(
        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:
        1. What is the customer's question?
        2. What information does the customer need?
        3. Provide a clear and helpful answer.

        Do not invent customer-specific facts or company policies.

        {feedback_section}
        """,
        expected_output="""
        Customer Question:
        Information Needed:
        Answer:
        """,
        agent=agent,
    )


# ============================================================
# ACCOUNT TASK
# ============================================================

def create_account_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None,
):
    feedback_section = ""

    if previous_response and qa_feedback:
        feedback_section = f"""
        PREVIOUS RESPONSE:
        {previous_response}

        QA FEEDBACK:
        {qa_feedback}

        Improve the previous response based on the QA feedback.

        CUSTOMER LOOKUP RULES:
        - If the ticket includes a customer ID and customer details
          are relevant, use the get_customer tool.
        - Base customer-specific statements on the tool result.
        - If the customer is not found, say so.
        - Never invent customer information.
        """

    return Task(
        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:
        1. What is the account-related problem?
        2. What steps should the customer take?
        3. Is there any security concern?
        4. Provide a clear resolution.

        ORDER LOOKUP RULES:
        - If the ticket asks about an order and provides an order ID,
          use the get_order_status tool.
        - Base order-specific statements on the tool result.
        - If the order is not found, clearly say so.
        - Never invent order status or delivery dates.

        For security incidents, prioritize appropriate official recovery
        and reporting channels. Do not claim that an action was completed
        when the support team has not performed it.

        {feedback_section}
        """,
        expected_output="""
        Account Problem:
        Security Concern:
        Recommended Steps:
        Resolution:
        """,
        agent=agent,
    )


# ============================================================
# QA TASK
# ============================================================

def create_qa_task(
    ticket,
    specialist_response,
    agent,
    retrieved_evidence="",
):
    evidence_section = (
        retrieved_evidence.strip()
        if retrieved_evidence and retrieved_evidence.strip()
        else "No support evidence was provided to QA."
    )

    return Task(
        description=f"""
        You are a strict quality assurance reviewer for customer support.

        CUSTOMER TICKET:
        {ticket}

        SPECIALIST RESPONSE:
        {specialist_response}

        RETRIEVED SUPPORT EVIDENCE:
        {evidence_section}

        REVIEW CRITERIA:

        1. DIRECTNESS
        Does the response address the customer's actual problem?

        2. ACCURACY
        Are factual claims supported by the ticket, retrieved tool results,
        or supplied support evidence?

        3. KNOWLEDGE BASE GROUNDING
        For technical troubleshooting, compare each product-specific
        recommendation and claimed cause against the retrieved evidence.

        Treat the supplied evidence as the source of truth for
        product-specific procedures and policies.

        4. SPECULATION
        Reject guesses presented as facts. A possible cause must not be
        presented as established without supporting evidence.

        5. DIAGNOSTIC QUESTIONS
        When information is insufficient, does the response ask relevant
        questions needed to investigate the problem?

        6. ESCALATION
        Does the response recommend appropriate escalation when necessary?

        7. CUSTOMER SAFETY
        Does the response avoid unsafe or unsupported instructions?

        8. CLARITY
        Is the response clear, relevant, and professional?

        STRICT APPROVAL RULES:

        Set approved=False if any significant issue exists, including:
        - Unsupported product-specific troubleshooting.
        - Invented root causes, updates, file-size limits, or policies.
        - Claims that contradict the supplied evidence.
        - Unsupported claims presented as confirmed facts.
        - Missing essential diagnostic questions or escalation.
        - Failure to address previous QA feedback.

        Do not approve a response simply because it sounds confident
        or is well written.

        If technical evidence was not supplied, do not pretend you
        verified the response against the knowledge base. Reject
        unsupported product-specific claims and explain the limitation.

        When rejecting, identify the specific unsupported claims and
        explain what must be removed or corrected.

        Approve only when the response meets the relevant criteria.
        """,
        expected_output="""
        Return a structured QA result matching the QAResult schema.

        approved:
        true or false

        feedback:
        Explain why the response passes. If rejected, identify specific
        issues and required corrections.
        """,
        agent=agent,
        output_pydantic=QAResult,
    )
