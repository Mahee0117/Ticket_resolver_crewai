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

        1. Category:
           Choose exactly one:
           Billing, Account, Technical, General

        2. Priority:
           Choose exactly one:
           Low, Medium, High, Urgent

        3. Issue:
           Provide a short description of the customer's problem.
        """,

        expected_output="""
        A structured triage result containing:

        - category
        - priority
        - issue
        """,

        output_pydantic=TriageResult,

        agent=agent
    )


# ============================================================
# BILLING TASK
# ============================================================

def create_billing_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None
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

        1. What is the billing problem?
        2. What should the customer do next?
        3. Provide a clear customer-friendly resolution.

        {feedback_section}
        ORDER LOOKUP RULES:
        - If the ticket asks about an order and provides an order ID,
        use the get_order_status tool to retrieve its status.
        - Base order-specific statements on the tool result.
        - If the order is not found, clearly say so.
        - Never invent order status or delivery dates.
        """,

        expected_output="""
        Billing Issue:
        Resolution:
        Next Step:
        """,

        agent=agent
    )


# ============================================================
# TECHNICAL TASK
# ============================================================


# ============================================================
# TECHNICAL TASK
# ============================================================

def create_technical_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None
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

        1. Before drafting the response, call the
           search_support_knowledge tool with a query relevant
           to the customer's technical issue.

        2. Read the retrieved documentation and use it as the
           source of truth for product-specific troubleshooting.

        3. Recommend only troubleshooting steps explicitly
           supported by the retrieved documentation.

        4. Do not invent root causes, product behavior, software
           updates, driver fixes, file-size limits, or other policies.

        5. If the documentation does not identify the root cause,
           explicitly state that the cause is not yet known.
           Do not fill this gap with guesses.

        6. If more information is needed, ask focused diagnostic
           questions relevant to the issue.

        7. If the documented steps have been tried and the issue
           persists, recommend escalation to the appropriate
           support team.

        8. If the knowledge base does not contain enough information,
           explain this limitation and ask for the information needed
           to investigate. Do not invent a solution.

        RESPONSE REQUIREMENTS:

        - Explain the reported technical problem.
        - State a possible cause only if the retrieved evidence
          actually supports it. Otherwise say "Cause not yet determined."
        - Provide only documented troubleshooting steps.
        - Ask relevant diagnostic questions when necessary.
        - Recommend escalation when appropriate.
        - Keep the customer-facing response concise and professional.

        {feedback_section}
        """,

        expected_output="""
        Technical Problem:
        Evidence-Based Cause:
        Troubleshooting:
        Information Needed:
        Resolution or Escalation:
        """,

        agent=agent
    )


# ============================================================
# GENERAL SUPPORT TASK
# ============================================================

def create_general_support_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None
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

        {feedback_section}
        """,

        expected_output="""
        Customer Question:
        Information Needed:
        Answer:
        """,

        agent=agent
    )


# ============================================================
# ACCOUNT TASK
# ============================================================

def create_account_task(
    ticket,
    agent,
    previous_response=None,
    qa_feedback=None
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
        - If the ticket includes a customer ID, use the get_customer tool
        to retrieve the record when customer details are relevant.
        - Base customer-specific statements on the tool result.
        - If the customer is not found, say the record could not be found.
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
        use the get_order_status tool to retrieve its status.
        - Base order-specific statements on the tool result.
        - If the order is not found, clearly say so.
        - Never invent order status or delivery dates.

        {feedback_section}
        """,

        expected_output="""
        Account Problem:
        Security Concern:
        Recommended Steps:
        Resolution:
        """,

        agent=agent
    )


# ============================================================
# QA TASK
# ============================================================

# ============================================================
# QA TASK
# ============================================================

def create_qa_task(ticket, specialist_response, agent):
    return Task(
        description=f"""
        You are a strict quality assurance reviewer for customer support.

        CUSTOMER TICKET:
        {ticket}

        SPECIALIST RESPONSE:
        {specialist_response}

        Evaluate the response against the following criteria.

        1. DIRECTNESS
        Does it address the customer's actual problem?

        2. ACCURACY
        Are factual claims supported by the ticket, retrieved tools,
        or available support documentation?

        3. KNOWLEDGE BASE GROUNDING
        For technical troubleshooting, check whether each
        product-specific recommendation is supported by the retrieved
        support documentation.

        Reject unsupported recommendations, including invented
        updates, driver fixes, file-size limits, root causes, or policies.

        4. SPECULATION
        Reject guesses presented as established facts.
        If the cause is unknown, the response must acknowledge this.

        5. DIAGNOSTIC QUESTIONS
        When information is insufficient, does the response ask
        relevant questions needed to investigate the problem?

        6. ESCALATION
        When documented troubleshooting is insufficient or the issue
        persists, does the response recommend appropriate escalation?

        7. RELEVANCE AND ACTIONABILITY
        Are the recommendations relevant and useful to this customer?

        8. CUSTOMER SAFETY
        Does the response avoid unnecessary or potentially harmful advice?

        9. CLARITY AND CONCISENESS
        Is the response professional, understandable, and free of
        unnecessary repetition?

        STRICT APPROVAL RULES:

        Set approved=False if ANY significant issue exists, especially:

        - A technical recommendation is not supported by the retrieved
          documentation.
        - A possible cause is presented as confirmed without evidence.
        - The response invents product behavior or company policy.
        - Necessary diagnostic information is missing.
        - Required escalation is omitted.
        - The response ignores previous QA feedback.

        Do not approve a response merely because it sounds confident,
        contains many steps, or is well written.

        If the response contains unsupported technical advice, reject it
        even if its other sections are good.

        If the knowledge base is insufficient, the specialist should
        acknowledge the limitation rather than invent a resolution.

        If rejected, give specific, actionable feedback identifying
        the unsupported claims and explaining what to remove or change.

        Approve only when the response meets the relevant criteria.
        """,

        expected_output="""
        Return a structured QA result matching the QAResult schema.

        approved:
        true or false

        feedback:
        Explain why the response passes the quality criteria.
        If rejected, identify specific issues and required corrections.
        """,

        agent=agent,
        output_pydantic=QAResult
    )
