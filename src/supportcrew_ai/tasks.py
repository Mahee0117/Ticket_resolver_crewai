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

        Improve the previous response based on the QA feedback.
        """

    return Task(

        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. What is the technical problem?
        2. What could be causing the problem?
        3. What troubleshooting steps should the customer follow?
        4. Provide a clear resolution.

        {feedback_section}
        """,

        expected_output="""
        Technical Problem:
        Possible Cause:
        Troubleshooting:
        Resolution:
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
def create_qa_task(ticket, specialist_response, agent):
    return Task(
        description=f"""
        Perform a strict quality review of the following customer support response.

        CUSTOMER TICKET:
        {ticket}

        SPECIALIST RESPONSE:
        {specialist_response}

        Evaluate the response using ALL of these criteria.

        1. DIRECTNESS
        Does the response directly address what the customer asked?

        2. ACCURACY
        Does the response avoid claims that cannot be supported by the ticket?

        3. RELEVANCE
        Is every major recommendation relevant to the customer's problem?

        4. ACTIONABILITY
        Does the response provide practical steps the customer can follow?

        5. CONCISENESS
        Is the response reasonably short for the customer's question?

        6. REPETITION
        Does the response repeat the same information or resolution multiple times?

        7. UNSUPPORTED ASSUMPTIONS
        Does the response assume details that the customer never provided?

        Examples:
        - assuming a specific operating system
        - assuming a specific application
        - assuming a specific company policy
        - inventing available account features
        - recommending another email address without justification

        8. SPECULATION
        Does the response present guesses or possible causes as if they were
        confirmed facts?

        9. CUSTOMER SAFETY
        Does the response avoid unnecessary or potentially harmful advice?

        10. PROFESSIONAL QUALITY
        Is the response clear, professional, understandable, and appropriate
        for a customer?

        STRICT APPROVAL RULE:

        APPROVE the response only when it is genuinely high quality.

        REJECT the response if there is a significant problem in any of these
        areas, especially:

        - unsupported recommendations
        - irrelevant troubleshooting
        - repeated information
        - excessive verbosity
        - speculative claims
        - missing important actions
        - assumptions not supported by the ticket

        IMPORTANT:

        Do NOT approve a response simply because it is long or contains many
        troubleshooting steps.

        A short and directly useful response is better than a long response
        containing unnecessary information.

        If the response is rejected, provide specific feedback that tells the
        specialist exactly what needs to be changed.
        """,

        expected_output="""
        Return a structured QA result.

        approved:
        true or false

        feedback:
        Explain why the response was approved.

        If rejected, identify the specific problems and explain how the
        specialist should improve the response.
        """,

        agent=agent,
        output_pydantic=QAResult
    )