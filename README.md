🤖 TalentScout Hiring Assistant

An AI-powered hiring assistant built with Streamlit, LangChain, OpenAI GPT, and Hugging Face Transformers.
This app collects candidate information, conducts technical interviews, performs sentiment analysis, and engages in interactive conversations.

🚀 Features

Candidate Information Form – Collects essential details like name, email, phone, experience, position, and tech stack.

AI-Powered Interview – Uses ChatOpenAI (gpt-3.5-turbo) to generate concise, role-specific technical interview questions.

Sentiment Analysis – Powered by Hugging Face transformers to evaluate candidate responses.

Interactive Chat Interface – Candidates can chat with the bot after submitting their details.

Session State Persistence – Maintains candidate info, chat history, and sentiment scores across interactions.

🛠️ Tech Stack

Streamlit
 – Web app framework

LangChain
 – LLM orchestration

OpenAI GPT
 – AI interview question generation

Hugging Face Transformers
 – Sentiment analysis

Python-dotenv
 – Environment variable management


📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/Basant2206/HiringAssistantchatbot_for_TalentScout_using_Streamlit_OpenAI.git
cd HiringAssistantchatbot_for_TalentScout_using_Streamlit_OpenAI

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key        

▶️ Run the App
streamlit run app.py


Then open 
Local URL: http://localhost:8501
Network URL: http://192.168.1.34:8501


📂 Project Structure
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
└── README.md               # Project documentation

🔮 Future Improvements
- Save candidate information to a database (e.g., PostgreSQL, Firebase).
- Add resume parsing for auto-filling candidate details.
- Enable multi-turn structured interview flow.
- Deploy on AWS / Streamlit Cloud / Docker.