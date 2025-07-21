import streamlit as st
import os
import base64
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="🧘‍♀️ Fitness and Diet Planner", layout="wide")

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Error: GROQ_API_KEY is missing. Check your .env file.")
    st.stop()

# Initialize Language Model
try:
    langchain_llm = ChatGroq(api_key=groq_api_key, model="llama3-8b-8192")
except Exception as e:
    st.error(f"Error initializing LLM: {e}")
    st.stop()


# Function to encode image in Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


# Apply background image
image_base64 = get_base64_image("static/img4.jpg")
if image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Define prompt templates
plan_prompt_template = """
You are a fitness and diet planner. Create two structured plans based on the user's input:
1. A **diet plan** table for {number_of_weeks} weeks.
2. A **workout plan** table for {number_of_weeks} weeks.

User Details:
- **Workout type**: {workout_type}
- **Diet type**: {diet_type}
- **Current weight**: {current_weight} kg
- **Target weight**: {target_weight} kg
- **Dietary restrictions**: {dietary_restrictions}
- **Health conditions**: {health_conditions}
- **Age**: {age}
- **Gender**: {gender}
- **Comments**: {comments}

Provide clear tables and key notes.
"""

plan_prompt = PromptTemplate(
    input_variables=[
        "workout_type", "diet_type", "current_weight", "target_weight", "dietary_restrictions",
        "health_conditions", "age", "gender", "number_of_weeks", "comments"
    ],
    template=plan_prompt_template,
)

chat_prompt_template = """
You are a fitness and diet expert. Answer the user's question based on their plan:

Plan: {plan}

Question: {question}

Provide a clear, detailed response.
"""

chat_prompt = PromptTemplate(input_variables=["plan", "question"], template=chat_prompt_template)

# Initialize chains
plan_chain = LLMChain(llm=langchain_llm, prompt=plan_prompt)
chat_chain = LLMChain(llm=langchain_llm, prompt=chat_prompt)

# App Title
st.title("🧘‍♀️ Fitness and Diet Planner")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("Enter Your Details:")
    workout_type = st.text_input("Workout Type (e.g., Weight Loss, Muscle Gain)")
    diet_type = st.text_input("Diet Type (e.g., Indian, Mediterranean)")
    current_weight = st.number_input("Current Weight (kg)", 30.0, 200.0, 75.0, 1.0)
    target_weight = st.number_input("Target Weight (kg)", 30.0, 200.0, 68.0, 1.0)
    dietary_restrictions = st.text_input("Dietary Restrictions (e.g., No dairy, Low sugar)")
    health_conditions = st.text_input("Health Conditions", "")
    age = st.number_input("Age", 10, 100, 30, 1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    number_of_weeks = st.slider("Number of Weeks", 1, 12, 4)
    comments = st.text_area("Additional Comments")

    if st.button("Generate Plans"):
        st.session_state["messages"] = []
        with st.spinner("Generating your personalized plans..."):
            try:
                response = plan_chain.run({
                    "workout_type": workout_type,
                    "diet_type": diet_type,
                    "current_weight": current_weight,
                    "target_weight": target_weight,
                    "dietary_restrictions": dietary_restrictions,
                    "health_conditions": health_conditions,
                    "age": age,
                    "gender": gender,
                    "number_of_weeks": number_of_weeks,
                    "comments": comments,
                })
                st.session_state.plan = response
                st.success("Plans generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

with col2:
    if "plan" in st.session_state and st.session_state.plan:
        st.header("Your Plans:")
        st.markdown(f'<div class="scrollable-response">{st.session_state.plan}</div>', unsafe_allow_html=True)

# Chat Section
if "plan" in st.session_state and st.session_state.plan:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Ask About Your Plan")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask a question about your plan"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            answer = chat_chain.run({"plan": st.session_state.plan, "question": prompt})
        except Exception as e:
            answer = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(answer)

# Footer
st.markdown("---")
st.caption("💡 Nextgen - AI Fitness and Diet Planner")
