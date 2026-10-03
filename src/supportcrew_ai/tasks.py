from crewai import Task

from supportcrew_ai.models import TriageResult


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

def create_billing_task(ticket, agent):

    return Task(

        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. What is the billing problem?
        2. What should the customer do next?
        3. Provide a clear customer-friendly resolution.
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

def create_technical_task(ticket, agent):

    return Task(

        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. What is the technical problem?
        2. What could be causing the problem?
        3. What troubleshooting steps should the customer follow?
        4. Provide a clear resolution.
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

def create_general_support_task(ticket, agent):

    return Task(

        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. What is the customer's question?
        2. What information does the customer need?
        3. Provide a clear and helpful answer.
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

def create_account_task(ticket, agent):

    return Task(

        description=f"""
        Analyze the following customer support ticket:

        {ticket}

        Determine:

        1. What is the account-related problem?
        2. What steps should the customer take?
        3. Is there any security concern?
        4. Provide a clear resolution.
        """,

        expected_output="""
        Account Problem:
        Security Concern:
        Recommended Steps:
        Resolution:
        """,

        agent=agent
    )