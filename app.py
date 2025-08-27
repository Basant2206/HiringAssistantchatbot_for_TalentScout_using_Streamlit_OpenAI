import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import json
load_dotenv()

if "sentiment_analyzer" not in st.session_state:
    from transformers import pipeline
    st.session_state.sentiment_analyzer = pipeline("sentiment-analysis")


def get_sentiment_hf(text):
    result = st.session_state.sentiment_analyzer(text)[0]
    return result["label"], result["score"]


# Initialize LLM
if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
         SystemMessage(content="""
            You are a technical interviewer. Generate 3-5 concise technical interview questions 
            to test a candidate skilled in: {tech_string}. 
            Questions should be relevant and challenging. Please do not deviate from the Purpose.
            Provide meaningful responses when You does not understand the user input or when unexpected inputs are received.
            Gracefully conclude the conversation, thanking the candidate and informing them about the next steps.
""")
    ]

def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
    st.title("🤖 TalentScout Hiring Assistant (LangChain)")

    if "candidate" not in st.session_state:
        st.session_state.candidate = {}

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    # Candidate form (only shows until submitted)
    if not st.session_state.submitted:
        st.write("👋 Hi! I’m *TalentScout Assistant*. Let’s collect your details first.")
        with st.form("candidate_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            exp = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
            position = st.text_input("Desired Position(s)")
            location = st.text_input("Current Location")
            tech_stack = st.text_area("Tech Stack (comma-separated)", 
                                    placeholder="e.g., Python, Django, React, SQL")
            submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.submitted = True
            st.session_state.candidate = {
                "name": name,
                "email": email,
                "phone": phone,
                "experience": exp,
                "position": position,
                "location": location,
                "tech_stack": [t.strip() for t in tech_stack.split(",") if t.strip()]
            }
            # Add candidate info to chat history + get first response
            st.session_state.chat_history.append(
                HumanMessage(content=json.dumps(st.session_state.candidate))
            )
            response = st.session_state.llm.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))
            st.experimental_rerun()   # force clean rerun after submit

    # Chat interface (only shows after submission)
    else:
        candidate = st.session_state.candidate
        st.subheader("✅ Candidate Information")
        st.json(candidate)

        st.subheader("💬 Conversation")
        for msg in st.session_state.chat_history:
            role = "🧑 You" if isinstance(msg, HumanMessage) else "🤖 Bot"
            if isinstance(msg, SystemMessage):
                continue
            if msg.content.startswith("{") and msg.content.endswith("}"):
                continue
            st.markdown(f"**{role}: ** {msg.content}")

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message:")
            chat_submit = st.form_submit_button("Send")

        if chat_submit and user_input:
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            label, score = get_sentiment_hf(user_input)
            st.session_state.sentiment = {"label": label, "score": score}
            response = st.session_state.llm.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))
            st.experimental_rerun()

        if "sentiment" in st.session_state:
            s = st.session_state.sentiment
            st.write(f"📊 Sentiment: {s['label']} (confidence={float(s['score']):.2f})")

        st.success(f"✅ Thanks {candidate['name']}! You can continue chatting.")
    

if __name__ == "__main__":
    main()
