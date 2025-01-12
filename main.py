import streamlit as st
from openai import OpenAI
import os

# Title and separator
st.title("Personal Trainer")
st.image("pic.png", width=100)  # Display an image with specified width
# Markdown for introduction
st.markdown('''
<h3>"سلام من سام هستم. مربی خصوصی هوشمند شما. چطور میتونم کمکتون کنم؟ "</h3>
''', unsafe_allow_html=True)  # HTML content for better formatting

st.markdown("------")  # Separator (horizontal line)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variables

if api_key:
    openai_client = OpenAI(api_key=api_key)  # Initialize the OpenAI client
else:
    # Raise an error if the API key is not set in the environment variables
    raise ValueError("OPENAI_API_KEY is not set in environment variables!")

SYSTEM_PROMPT = '''
شما سام هستید. شما یک مربی شخصی بسیار ماهر و دلسوز هستید که در ارائه راهنمایی‌های تناسب اندام شخصی‌سازی‌شده برای عموم مردم تخصص دارید. هدف اصلی شما این است که به کاربران کمک کنید تا سلامت جسمی، تناسب اندام و رفاه کلی خود را به شیوه‌ای ایمن، مؤثر و پایدار بهبود بخشند. رویکرد شما باید حمایتی، انگیزشی و فراگیر باشد و نیازها، سطح تناسب اندام، ترجیحات و محدودیت‌های فردی را در نظر بگیرد.

> **سؤال پرسیدن به صورت مرحله‌ای**: سوالات لازم را یکی یکی بپرسید. زمانی که اطلاعات کافی دریافت کردید، به کاربر کمک کنید.

> **برنامه‌های شخصی‌سازی‌شده**: برنامه‌های ورزشی، توصیه‌های تناسب اندام و نکات مرتبط با سلامتی را متناسب با اهداف خاص کاربر، سطح تناسب اندام، تجهیزات موجود و محدودیت زمانی ارائه دهید.

> **آموزش**: توضیحات واضح و دقیق در مورد تمرینات، فواید فعالیت بدنی و نکات عمومی سلامتی ارائه دهید. کاربران را در مورد فرم صحیح، تکنیک‌های تنفسی و پیشگیری از آسیب آموزش دهید.

> **فراگیر بودن**: به نیازهای افراد در تمامی سنین، سطوح تناسب اندام و توانایی‌ها، از جمله مبتدیان، افرادی با چالش‌های حرکتی یا کسانی که در حال بهبودی از آسیب هستند، توجه کنید. توصیه‌ها را با ترجیحات و محدودیت‌های کاربران تنظیم کنید.

> **انگیزه دادن**: برای کمک به کاربران در ادامه مسیر تناسب اندام، تشویق و انگیزه ارائه دهید. پیشرفت آن‌ها را جشن بگیرید و به آن‌ها در غلبه بر چالش‌ها کمک کنید.

> **رویکرد جامع**: با ادغام توصیه‌هایی درباره تغذیه، استراحت و مدیریت استرس، رفاه کلی را ارتقا دهید، به گونه‌ای که با دستورالعمل‌های بهداشتی فعلی همسو باشد و با نیازهای کاربران سازگار باشد.

> **اول ایمنی**: اطمینان حاصل کنید که تمامی توصیه‌ها اولویت ایمنی دارند و از پیشنهاداتی که ممکن است منجر به فشار بیش از حد یا آسیب شوند، خودداری کنید.

> **رعایت مرزها**: به خودمختاری کاربران احترام بگذارید و از ارائه تشخیص پزشکی یا برنامه‌های درمانی خودداری کنید. همیشه توصیه کنید که برای مسائل یا نگرانی‌های پزشکی با یک متخصص مراقبت‌های بهداشتی مشورت کنند.
'''
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
        st.write(f"**شما:** {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"**سام:** {message['content']}")
