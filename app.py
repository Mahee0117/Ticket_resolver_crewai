
import streamlit as st

from supportcrew_ai.main import process_ticket


st.set_page_config(
    page_title="SupportCrew AI",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 SupportCrew AI")
st.caption("Multi-agent customer support · Tools · RAG · Quality Assurance")

st.divider()

# -------------------------
# Ticket input
# -------------------------

st.subheader("Submit a support ticket")

examples = {
    "Technical — PDF upload crash":
        "The application crashes whenever I try to upload a PDF.",
    "Account — Password reset":
        "I forgot my password and cannot log in. The reset email is not arriving.",
    "Billing — Order status":
        "My order shows the wrong delivery status. Order ID: ORD101",
    "Security — Unauthorized access":
        "Someone has gained unauthorized access to my account and I see transactions I did not make.",
}

selected_example = st.selectbox(
    "Try an example ticket",
    ["None"] + list(examples.keys()),
)

default_ticket = (
    examples[selected_example]
    if selected_example != "None"
    else ""
)

ticket = st.text_area(
    "Describe the customer's issue",
    value=default_ticket,
    height=150,
    placeholder="Enter the customer's problem here...",
)

analyze = st.button(
    "Analyze Ticket",
    type="primary",
    use_container_width=True,
)

# -------------------------
# Run actual CrewAI workflow
# -------------------------

if analyze:
    if not ticket.strip():
        st.warning("Please enter a support ticket.")
    else:
        try:
            with st.spinner(
                "CrewAI is classifying the ticket, consulting the specialist, and running QA..."
            ):
                result = process_ticket(ticket.strip())

            st.divider()
            st.header("Analysis Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Category", result["category"])

            with col2:
                st.metric("Priority", result["priority"])

            with col3:
                st.metric("Attempts", result["attempts"])

            st.subheader("Issue Summary")
            st.write(result["issue"])

            st.subheader("Specialist Response")
            st.markdown(result["response"])

            st.subheader("Quality Assurance")

            if result["qa_approved"]:
                st.success(
                    f"Response approved after {result['attempts']} attempt(s)."
                )
            else:
                st.error(
                    "The response did not pass QA within the retry limit. "
                    "It has not been approved."
                )

            with st.expander("QA feedback"):
                st.write(result["qa_feedback"])

            if result["evidence"]:
                with st.expander("Retrieved support documentation"):
                    st.markdown(result["evidence"])

            st.download_button(
                "Download analysis",
                data=(
                    f"SupportCrew AI Analysis\n\n"
                    f"Category: {result['category']}\n"
                    f"Priority: {result['priority']}\n"
                    f"Issue: {result['issue']}\n\n"
                    f"Specialist Response:\n{result['response']}\n\n"
                    f"QA Approved: {result['qa_approved']}\n"
                    f"Attempts: {result['attempts']}\n"
                    f"QA Feedback: {result['qa_feedback']}\n"
                ),
                file_name="support_ticket_analysis.txt",
                mime="text/plain",
            )

        except Exception as exc:
            st.error(f"Ticket processing failed: {exc}")
            st.info(
                "Check that Ollama is running, the configured model is available, "
                "and the support knowledge base is initialized."
            )

st.divider()
st.caption("SupportCrew AI · CrewAI + Ollama + ChromaDB + Streamlit")
