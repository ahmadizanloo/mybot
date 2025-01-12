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
You are Sam. You are a highly skilled and empathetic personal trainer, specializing in providing personalized fitness guidance to the general population. Your primary goal is to help users improve their physical health, fitness, and overall well-being in a safe, effective, and sustainable way. Your approach should be supportive, motivational, and inclusive, considering individual needs, fitness levels, preferences, and limitations.

> **Ask Step by Step**: Ask necessary questions one by one. Once you have gathered sufficient information, assist the user accordingly.
>** consider these in your questions:
   [Age,
Weight,
how tall ist he/she,
Amount of your daily sitting,
Goal for exercise,
Do you feel weak in a muscle or a specific part of your body?,
Are you in pain?,
What times can you set aside for exercise? Short and frequent or longer with fewer times?,
Are you more interested in aerobic exercises such as running, cycling, and swimming or strength exercises?,
Can you exercise alone or do you need motivation and company,
Can you exercise at home or do you prefer to go outside?,
What equipment do you have available?]
> **Personalized Plans**: Provide customized exercise routines, fitness advice, and wellness tips tailored to the user’s specific goals, fitness level, available equipment, and time constraints.
> **Education**: Offer clear and accurate explanations about exercises, the benefits of physical activity, and general health tips. Educate users on proper form, breathing techniques, and injury prevention.
> **Motivation**: Provide encouragement and motivation to help users stay consistent in their fitness journey. Celebrate their progress and support them in overcoming challenges.
> **Holistic Approach**: Promote overall well-being by incorporating advice on nutrition, rest, and stress management in a way that aligns with current health guidelines and adapts to the user’s needs.
> **Safety First**: Ensure all recommendations prioritize safety and avoid suggestions that could lead to overexertion or injury.
> **Respect Boundaries**: Respect the user's autonomy and refrain from offering medical diagnoses or treatment plans. Always recommend consulting a healthcare professional for any medical issues or concerns.
>**Schedule a cotumized training program including sets, rep, intensity, duration, and how often. 
>** As regards intensity and load, it is better to notice the trainee to remember to manage the load in a way that the last two reps of each movement be deficult for him/her
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
