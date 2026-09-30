import warnings

warnings.filterwarnings("ignore")

import os

from dotenv import load_dotenv
from pydantic import BaseModel
from crewai import Agent, Crew, Task, LLM


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

print("HF token loaded:", bool(hf_token))


# ============================================================
# 2. CONFIGURE LLM
# ============================================================

llm = LLM(
    model="openai/gpt-oss-120b:groq",
    api_key=hf_token,
    base_url="https://router.huggingface.co/v1",
    provider="openai"
)


# ============================================================
# 3. DEFINE STRUCTURED TRIAGE OUTPUT
# ============================================================

class TriageResult(BaseModel):

    category: str
    priority: str
    issue: str


# ============================================================
# 4. CREATE TRIAGE AGENT
# ============================================================

triage_agent = Agent(

    role="Senior Customer Support Triage Specialist",

    goal="""
    Analyze customer support tickets and classify each ticket
    into a supported category and priority.

    Provide a concise summary of the customer's issue.
    """,

    backstory="""
    You are a senior customer support triage specialist.

    Your responsibility is to analyze incoming customer
    support tickets and determine where each ticket should
    be routed.

    Supported categories:

    - Billing: payments, refunds, duplicate charges, subscriptions
    - Account: login, password, account access, profile problems
    - Technical: bugs, crashes, errors, application failures
    - General: general questions and information requests

    Priority levels:

    - Low: general questions or issues with little immediate impact
    - Medium: customer is blocked but there is no major financial
      or critical impact
    - High: financial problems, significant functionality problems,
      or important account issues
    - Urgent: severe problems requiring immediate attention

    Always use exactly one supported category and one supported
    priority level.
    """,

    llm=llm,

    verbose=False
)


# ============================================================
# 5. CREATE SPECIALIST AGENTS
# ============================================================

Billing_agent = Agent(

    role="Senior Billing Support Specialist",

    goal="""
    Resolve customer issues related to payments, refunds,
    duplicate charges, and subscriptions.
    """,

    backstory="""
    You are an experienced billing support specialist.

    You investigate billing-related customer problems,
    explain the issue clearly, and provide an appropriate
    resolution or next step.
    """,

    llm=llm,

    verbose=False
)


Technical_agent = Agent(

    role="Senior Technical Support Specialist",

    goal="""
    Diagnose and resolve customer issues involving
    application bugs, crashes, errors, and technical failures.
    """,

    backstory="""
    You are an experienced technical support specialist.

    You analyze technical problems reported by customers,
    identify the likely cause from the information provided,
    and provide practical troubleshooting steps or a resolution.
    """,

    llm=llm,

    verbose=False
)


General_support_agent = Agent(

    role="Senior General Customer Support Specialist",

    goal="""
    Handle general customer questions and provide
    clear, helpful, and accurate information.
    """,

    backstory="""
    You are an experienced customer support specialist
    who handles general customer questions.

    You communicate clearly and professionally and
    provide simple instructions that customers can follow.
    """,

    llm=llm,

    verbose=False
)


Account_agent = Agent(

    role="Senior Account Support Specialist",

    goal="""
    Resolve customer issues related to account access,
    passwords, login problems, profiles, and account security.
    """,

    backstory="""
    You are an experienced account support specialist.

    You handle login problems, password issues,
    account access problems, profile issues,
    and account security concerns.

    You provide safe and clear guidance to customers
    without requesting sensitive credentials.
    """,

    llm=llm,

    verbose=False
)


# ============================================================
# 6. CREATE TEST TICKETS
# ============================================================

ticket1 = """
I forgot my password and I cannot log into my account.
The password reset email is not arriving.
"""


ticket2 = """
The application crashes whenever I try to upload a PDF.
"""


ticket3 = """
How can I change my profile picture?
"""


ticket4 = """
Someone has gained unauthorized access to my account
and I can see transactions that I did not make.
Please help immediately.
"""


tickets = [
    ticket1,
    ticket2,
    ticket3,
    ticket4
]


# ============================================================
# 7. PROCESS EACH TICKET
# ============================================================

for ticket in tickets:

    # ========================================================
    # 7A. CREATE TRIAGE TASK
    # ========================================================

    triage_task = Task(

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

        agent=triage_agent
    )


    # ========================================================
    # 7B. CREATE BILLING TASK
    # ========================================================

    billing_task = Task(

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

        agent=Billing_agent
    )


    # ========================================================
    # 7C. CREATE TECHNICAL TASK
    # ========================================================

    technical_task = Task(

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

        agent=Technical_agent
    )


    # ========================================================
    # 7D. CREATE GENERAL SUPPORT TASK
    # ========================================================

    general_support_task = Task(

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

        agent=General_support_agent
    )


    # ========================================================
    # 7E. CREATE ACCOUNT TASK
    # ========================================================

    account_task = Task(

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

        agent=Account_agent
    )


    # ========================================================
    # 8. RUN TRIAGE CREW
    # ========================================================

    triage_crew = Crew(

        agents=[triage_agent],

        tasks=[triage_task],

        verbose=False
    )


    triage_result = triage_crew.kickoff()


    # ========================================================
    # 9. GET STRUCTURED TRIAGE RESULT
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
    # 10. ROUTE TO SPECIALIST AGENT
    # ========================================================

    category = triage_data.category


    if category == "Billing":

        specialist_crew = Crew(

            agents=[Billing_agent],

            tasks=[billing_task],

            verbose=False
        )

        specialist_result = specialist_crew.kickoff()


        print("\n========== BILLING RESULT ==========")

        print(specialist_result)


    elif category == "Technical":

        specialist_crew = Crew(

            agents=[Technical_agent],

            tasks=[technical_task],

            verbose=False
        )

        specialist_result = specialist_crew.kickoff()


        print("\n========== TECHNICAL RESULT ==========")

        print(specialist_result)


    elif category == "Account":

        specialist_crew = Crew(

            agents=[Account_agent],

            tasks=[account_task],

            verbose=False
        )

        specialist_result = specialist_crew.kickoff()


        print("\n========== ACCOUNT RESULT ==========")

        print(specialist_result)


    elif category == "General":

        specialist_crew = Crew(

            agents=[General_support_agent],

            tasks=[general_support_task],

            verbose=False
        )

        specialist_result = specialist_crew.kickoff()


        print("\n========== GENERAL SUPPORT RESULT ==========")

        print(specialist_result)


    else:

        print("\nUnknown category:", category)