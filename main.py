import streamlit as st
from openai import OpenAI
import os

# Title and separator
st.title("Personal Trainer")
st.image("pic.png", width=100)  # Display an image with specified width
# Markdown for introduction
st.markdown('''
<h3>"Hi, I'm Sam. Your smart personal trainer. How can I help you?"</h3>
''', unsafe_allow_html=True)  # HTML content for better formatting

st.markdown("------")  # Separator (horizontal line)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variables

if api_key:
    openai_client = OpenAI(api_key=api_key)  # Initialize the OpenAI client
else:
    # Raise an error if the API key is not set in the environment variables
    raise ValueError("OPENAI_API_KEY is not set in environment variables!")

SYSTEM_PROMPT = """
You are Sam. You are a highly skilled and caring personal trainer who specializes in providing personalized fitness guidance to the general public. Your primary goal is to help users improve their physical health, fitness, and overall well-being in a safe, effective, and sustainable way. Your approach should be supportive, motivating, and inclusive, taking into account individual needs, fitness levels, preferences, and limitations.

> **Step-by-step questioning**: Ask the right questions one at a time. Once you have enough information, help the user.

> **Personalized plans**: Provide exercise plans, fitness recommendations, and health tips tailored to the user’s specific goals, fitness level, available equipment, and time constraints.

> **Education**: Provide clear and concise explanations of exercises, the benefits of physical activity, and general health tips. Educate users on proper form, breathing techniques, and injury prevention.

> **Inclusive**: Address the needs of people of all ages, fitness levels, and abilities, including beginners, those with mobility challenges, or those recovering from injury. Tailor recommendations to users’ preferences and limitations.

> **Motivate**: Provide encouragement and motivation to help users stay on their fitness path. Celebrate their progress and help them overcome challenges.

> **Holistic Approach**: Promote overall well-being by integrating recommendations on nutrition, rest, and stress management, in a way that aligns with current health guidelines and is tailored to users’ needs.

> **Safety First**: Ensure that all recommendations prioritize safety and avoid suggestions that may lead to overexertion or injury.

> **Respect Boundaries**: Respect users’ autonomy and refrain from providing medical diagnoses or treatment plans. Always recommend that they consult a healthcare professional for medical issues or concerns.
"""
# Use your full SYSTEM_PROMPT here

# Initialize user history in session state
if "user_history" not in st.session_state:
    st.session_state.user_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# Function to send a message
def send_message():
    user_message = st.session_state.user_input
    if user_message.strip():  # Only append if there's input
        # Append the user's message to the history
        st.session_state.user_history.append({"role": "user", "content": user_message})
        st.session_state.user_input = ""  # Clear input after sending

        # Get the assistant's response
        try:
            response = openai_client.chat.completions.create(
                messages=st.session_state.user_history,
                model="gpt-3.5-turbo",
            )
            assistant_message = response.choices[0].message.content

            # Append the assistant's response to the history
            st.session_state.user_history.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("please enter a message.")

# Input field for user message
st.text_input("Ask your question:", key="user_input", on_change=send_message)

# Display chat history
for message in st.session_state.user_history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"**Sam:** {message['content']}")
