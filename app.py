import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# ---------- MUST BE FIRST STREAMLIT COMMAND ----------
st.set_page_config(page_title="Freelance Finance Bot", page_icon="💰")

# ---------- LOAD API KEY ----------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ---------- CHECK API KEY ----------
if not API_KEY:
    st.error("🚨 GEMINI_API_KEY not found. Please create a `.env` file with your key.")
    st.stop()

# ---------- INITIALIZE GEMINI CLIENT (new SDK) ----------
client = genai.Client(api_key=API_KEY)

# ---------- SYSTEM PROMPT + FEW‑SHOT + GUARDRAILS ----------
SYSTEM_PROMPT = """
You are a Personal Finance Assistant for freelancers in the US.
Your expertise: estimated taxes, deductible expenses (home office, equipment, software), retirement plans (SEP IRA, Solo 401k), invoicing, and budgeting.

Strict rules:
- Do NOT give legal or binding tax advice.
- Always recommend consulting a CPA for personalized guidance.
- Never request or store personal financial data (SSN, bank details).
- For out‑of‑scope questions (sports, medical, entertainment), politely refuse.

Tone: friendly, practical, encouraging.

Few‑shot examples:

User: "How much should I save for quarterly taxes?"
Assistant: "A common rule for freelancers is to save 25–30% of net income for federal + state taxes. For $60k/year, that's ~$15k–$18k total, or $3,750–$4,500 per quarter. Use IRS Form 1040‑ES. Confirm with a CPA."

User: "Can I deduct my new laptop?"
Assistant: "Yes, if used >50% for freelance work. You may deduct the full cost in one year (Section 179) or depreciate over time. Keep receipts and a business‑use log. Ask a CPA which method is best for you."

User: "What's the safest emergency fund for freelancers?"
Assistant: "Because income varies, aim for 6–12 months of essential expenses. If you spend $3,000/month on rent, food, insurance, save $18,000–$36,000 in a high‑yield savings account."

Out‑of‑scope guardrail:
User: "Who won the Super Bowl?"
Assistant: "I'm a finance assistant for freelancers. I can't answer sports questions. Please ask about taxes, deductions, budgeting, or retirement."
"""

# ---------- INITIALIZE SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- HELPER: LOG FEEDBACK ----------
def log_feedback(user_msg, bot_msg, rating):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_msg,
        "rating": rating  # "positive" or "negative"
    }
    with open("feedback_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

# ---------- UI ----------
st.title("💰 Freelance Finance Assistant")
st.markdown("Ask about **taxes, deductions, budgeting, retirement** – for US freelancers.")

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and i > 0:
            col1, col2 = st.columns(2)
            user_msg = st.session_state.messages[i-1]["content"]
            if col1.button("👍", key=f"up_{i}"):
                log_feedback(user_msg, msg["content"], "positive")
                st.success("Thank you!")
            if col2.button("👎", key=f"down_{i}"):
                log_feedback(user_msg, msg["content"], "negative")
                st.warning("Feedback recorded. We'll improve!")

# Chat input
if prompt := st.chat_input("Example: 'What home office expenses can I deduct?'"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history for Gemini
    history = ""
    for m in st.session_state.messages[:-1]:  # exclude latest user message
        history += f"{m['role'].capitalize()}: {m['content']}\n"
    full_prompt = SYSTEM_PROMPT + "\n\n" + history + f"User: {prompt}\nAssistant:"

    # ---- MODEL CONFIGURATION (using confirmed available models) ----
    # The model name MUST include "models/" prefix
    model_names_to_try = [
        "models/gemini-2.5-flash",   # best and fastest (confirmed in list_models.py)
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest"
    ]
    bot_reply = None
    for model_name in model_names_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )
            bot_reply = response.text
            break  # exit loop on first success
        except Exception as e:
            # Try next model
            continue

    if bot_reply is None:
        bot_reply = "⚠️ No working model found. Please check your API key or internet connection."

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Rerun to show new feedback buttons
    st.rerun()

# ---------- SIDEBAR: EVALUATION EXPORT ----------
with st.sidebar:
    st.header("📊 Evaluation")
    if st.button("Download Feedback Log"):
        if os.path.exists("feedback_log.jsonl"):
            with open("feedback_log.jsonl", "r") as f:
                lines = f.readlines()
            if lines:
                import pandas as pd
                data = [json.loads(line) for line in lines]
                df = pd.DataFrame(data)
                st.download_button("Export CSV", df.to_csv(index=False), "feedback.csv")
            else:
                st.info("No feedback yet. Use thumbs up/down.")
        else:
            st.info("No feedback file found.")