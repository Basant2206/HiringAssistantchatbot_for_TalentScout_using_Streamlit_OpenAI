# app_langchain.py
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
load_dotenv()

# Initialize LLM

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# Conversation memory to maintain context
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Build prompt with memory support
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful hiring assistant."),
    ("human", "{input}"),
])

#from langchain.chains import LLMChain
#conversation = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)
# Build modern chain (RunnableSequence instead of LLMChain)
chain = prompt | llm


# Streamlit App

def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
    st.title("🤖 TalentScout Hiring Assistant (LangChain)")

    # Greeting
    st.write("👋 Hi! I’m *TalentScout Assistant*. Let’s collect your details and generate some technical questions.")

    if "candidate" not in st.session_state:
        st.session_state.candidate = {}
        st.session_state.submitted = False

    # Candidate info collection
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

    # After submission
    if st.session_state.submitted:
        candidate = st.session_state.candidate
        st.subheader("✅ Candidate Information")
        st.json(candidate)

        # Building dynamic prompt
        tech_string = ", ".join(candidate["tech_stack"])
        question_prompt = ChatPromptTemplate.from_template(
            "You are a technical interviewer. Generate 3-5 concise technical interview questions "
            "to test a candidate skilled in: {tech_string}. "
            "Questions should be relevant and challenging."
        )

        # Formatting prompt correctly
        messages = question_prompt.format_messages(tech_string=tech_string)

        # Calling the LLM with formatted messages
        response = llm.invoke(messages)

        st.subheader("📌 Technical Questions")
        for line in response.content.split("\n"):
            if line.strip():
                st.write(f"- {line.strip()}")

        # End conversation
        st.success(f"✅ Thanks {candidate['name']}! Your responses are recorded.")

if __name__ == "__main__":
    main()
