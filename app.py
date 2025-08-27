import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import json

load_dotenv()

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

    # Greeting
    st.write("👋 Hi! I’m *TalentScout Assistant*. Let’s collect your details and generate some technical questions.")
    candidate = {}
    if "candidate" not in st.session_state:
        st.session_state.candidate = {}
        st.session_state.submitted = False

    # Candidate info collection
    if not st.session_state.submitted:
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

            # Add candidate info into chat history
            st.session_state.chat_history.append(
                HumanMessage(content=json.dumps(st.session_state.candidate))
            )

            # Generate first batch of questions
            response = st.session_state.llm.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))
            

    # After submission → chat mode
    if st.session_state.submitted:
        candidate = st.session_state.candidate
        st.subheader("✅ Candidate Information")
        st.json(candidate)
        
        # Display conversation 
        
        st.subheader("💬 Conversation")
        for msg in st.session_state.chat_history:
            role = "🧑 You" if isinstance(msg, HumanMessage) else "🤖 Bot"
            if isinstance(msg, SystemMessage):
                continue
            if "name" in msg.content:
                continue
            
            st.markdown(f"**{role}: ** {msg.content}")

        # 2. Input box at the BOTTOM
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message:")
            submitted = st.form_submit_button("Submite")

        if submitted and user_input:
            # Add user message
            st.session_state.chat_history.append(HumanMessage(content=user_input))

            # Get bot response
            response = st.session_state.llm.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))

            st.experimental_rerun()

        # Continue chatting
        st.success(f"✅ Thanks {candidate['name']}! You can continue chatting.")
    #print(st.session_state.chat_history)
    

if __name__ == "__main__":
    main()
