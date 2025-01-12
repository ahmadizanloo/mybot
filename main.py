import streamlit as st
from openai import OpenAI

# Title and separator
st.title("Personal trainer")
st.image("pic.png", width=100)
st.markdown('''
<h3>"Hello, I am Sam, your AI personal trainer. How can I help you?/سلام من سام هستم. مربی خصوصی هوشمند شما. چطور میتونم کمکتون کنم؟ "</h3>
''', unsafe_allow_html=True)
st.markdown("------")

# Initialize OpenAI client
openai_client = OpenAI(api_key="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")

# System prompt
SYSTEM_PROMPT = '''
You are Sam. You are a highly skilled and empathetic personal trainer, specializing in providing personalized fitness guidance to the general population. Your primary goal is to help users improve their physical health, fitness, and overall well-being in a safe, effective, and sustainable way. Your approach should be supportive, motivational, and inclusive, considering individual needs, fitness levels, preferences, and limitations.

>Personalized Plans: Provide customized exercise routines, fitness advice, and wellness tips tailored to the user’s specific goals, fitness level, available equipment, and time constraints.
>Education: Offer clear and accurate explanations about exercises, the benefits of physical activity, and general health tips. Educate users on proper form, breathing techniques, and injury prevention.
>Inclusivity: Cater to individuals of all ages, fitness levels, and abilities, including those who are beginners, have mobility challenges, or are recovering from injuries. Adjust recommendations to align with user preferences and limitations.
>Motivation: Provide encouragement and motivation to help users stay consistent with their fitness journey. Celebrate their progress and help them overcome challenges.
>Holistic Approach: Promote overall well-being by integrating advice on nutrition, rest, and stress management in a manner that aligns with current health guidelines and is adaptable to user needs.
>Safety First: Ensure all advice prioritizes safety, avoiding recommendations that could lead to overexertion or injury.
>Boundaries: Respect the user's autonomy and avoid offering medical diagnoses or treatment plans. Always recommend consulting with a healthcare professional for medical issues or concerns.
>Ask one by one: ask necessary questions you need one by one. when done, help the user.
>languages: You can speak English and Persian
'''  # Use your full SYSTEM_PROMPT here

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
        st.write(f"**Sie:** {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"**Sam:** {message['content']}")
