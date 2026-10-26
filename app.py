import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.set_page_config(page_title="PerspectiveAI", page_icon="✍️", layout="centered")
st.title("✍️ PerspectiveAI")
st.caption("Turn your real project experiences and lessons into authentic social content.")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is missing. Add it to your .env file and restart the app.")
    st.code('GOOGLE_API_KEY="copy your key here"', language="text")
    st.stop()

@st.cache_resource
def get_model():
    # Change the model ID if it is not available for your API key.
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_retries=2,
    )

model = get_model()
parser = StrOutputParser()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "draft" not in st.session_state:
    st.session_state.draft = ""

with st.sidebar:
    st.header("Content settings")
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram Stories", "Telegram community"],
    )
    tone = st.selectbox(
        "Tone",
        ["Natural and personal", "Professional", "Casual and friendly",
         "Reflective storytelling", "Technical and informative"],
    )
    language = st.selectbox("Language", ["English", "Tamil", "Simple English"])
    length = st.selectbox("Length", ["Short", "Medium", "Detailed"])
    st.divider()
    if st.button("Start a new conversation"):
        st.session_state.messages = []
        st.session_state.draft = ""
        st.rerun()

# Show conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input(
    "Tell me about your project, experience, challenge, or lesson learned..."
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    system_prompt = """
You are PerspectiveAI, a thoughtful personal content-writing assistant.

Your job:
1. Understand the user's actual project, experience, opinion, challenge, and lessons learned.
2. Ask at most ONE concise follow-up question if essential information is missing.
3. If enough information is available, create content for the selected platform.
4. Preserve the user's perspective and natural voice.
5. Never invent achievements, results, project details, credentials, quotes, or lessons.
   If something is unknown, omit it or ask the user.
6. Avoid generic hype and exaggerated claims.
7. Do not generate the final post yet if you need clarification. Ask the follow-up question instead.
8. If the user explicitly asks to draft, generate, revise, shorten, or translate content,
   do that directly using the information already provided.
9. Do not claim to publish content. You only prepare drafts.

Platform guidance:
- LinkedIn: readable personal/professional post, useful learning, optional relevant hashtags.
- Instagram Stories: create 3–5 slides, each with a short heading and concise text.
  You may suggest a visual for each slide, but do not require one.
- Telegram community: friendly, clear community post, with an optional discussion question.

Output settings:
Platform: {platform}
Tone: {tone}
Language: {language}
Length: {length}

Keep the answer easy to copy. When drafting, return the content itself and avoid explaining your
internal process. When the user is still describing their experience, respond conversationally.
"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{history}"),
        ("human", "{input}"),
    ])
    chain = prompt | model | parser

    # Use previous turns, excluding the newest user message (passed separately as input).
    history = []
    for old_msg in st.session_state.messages[:-1]:
        history.append((old_msg["role"], old_msg["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = chain.invoke({
                    "platform": platform,
                    "tone": tone,
                    "language": language,
                    "length": length,
                    "history": history,
                    "input": user_input,
                })
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.draft = answer
            except Exception as exc:
                st.error(
                    "The model request failed. Check your API key, model availability, "
                    "internet connection, and installed packages."
                )
                st.caption(f"Technical detail: {exc}")

if st.session_state.draft:
    st.divider()
    st.subheader("Latest response")
    st.download_button(
        "Download latest response as .txt",
        data=st.session_state.draft,
        file_name="perspectiveai_draft.txt",
        mime="text/plain",
    )
    revised_text = st.text_area(
        "Edit the draft yourself (optional)",
        value=st.session_state.draft,
        height=220,
        key="manual_edit",
    )
    if st.button("Save my edits"):
        st.session_state.draft = revised_text
        st.success("Edits saved for this session. Download the updated draft above.")
