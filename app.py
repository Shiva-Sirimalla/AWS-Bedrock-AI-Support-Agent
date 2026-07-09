import streamlit as st
from config import get_bedrock_client, get_dynamodb_client
from agent import agent_response
import json
from datetime import datetime

st.set_page_config(page_title="AWS Bedrock AI Support Agent", layout="wide")

st.title("🚀 AWS Bedrock AI Support Agent")
st.markdown("Powered by AWS Bedrock • Llama 3 8B Instruct")

# Quick reply suggestions
QUICK_REPLIES = [
    "How long does delivery take?",
    "What's your refund policy?",
    "I need technical support",
    "Can I track my order?",
    "How do I cancel?",
]

# Sidebar for credentials
with st.sidebar:
    st.header("⚙️ Configuration")
    access_key = st.text_input("AWS Access Key", type="password")
    secret_key = st.text_input("AWS Secret Key", type="password")
    
    st.markdown("---")
    st.subheader("📊 Chat Analytics")
    if "messages" in st.session_state and st.session_state.messages:
        total_msgs = len(st.session_state.messages)
        user_msgs = len([m for m in st.session_state.messages if m[0] == "You"])
        agent_msgs = len([m for m in st.session_state.messages if m[0] == "Agent"])
        
        col1, col2 = st.columns(2)
        col1.metric("Total Messages", total_msgs)
        col2.metric("User Messages", user_msgs)
        st.metric("Agent Responses", agent_msgs)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Chat"):
            st.session_state.export_requested = True
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.ratings = {}
            st.rerun()

bedrock_available = False
bedrock = None

if access_key and secret_key:
    try:
        bedrock = get_bedrock_client(access_key, secret_key)
        dynamodb = get_dynamodb_client(access_key, secret_key)
        table = dynamodb.Table("chat_memory")
        
        # Test the connection
        bedrock.list_foundation_models()
        bedrock_available = True
        
    except Exception as e:
        error_str = str(e)
        if "AccessDeniedException" in error_str or "not authorized" in error_str:
            st.sidebar.error("❌ AWS IAM Permission Denied")
            st.sidebar.info("Your AWS user lacks Bedrock permissions. Running in Demo Mode with sample responses.")
        else:
            st.sidebar.warning(f"⚠️ AWS Error: {error_str}")
        bedrock = None
        bedrock_available = False

if "messages" not in st.session_state:
    st.session_state.messages = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

# Input area at top
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("Ask your question:", placeholder="Type your message here...", key="main_input")

with col2:
    send_button = st.button("Send 📤", use_container_width=True)

# Quick reply buttons
st.markdown("**💡 Quick replies:**")
quick_cols = st.columns(len(QUICK_REPLIES))
for idx, reply in enumerate(QUICK_REPLIES):
    if quick_cols[idx].button(reply, key=f"quick_{idx}"):
        user_input = reply
        send_button = True

# Process message
final_input = user_input if send_button and user_input.strip() else None

if final_input:
    st.session_state.messages.append(("You", final_input))
    
    typing_placeholder = st.empty()
    typing_placeholder.info("🤖 Agent is thinking...")
    
    try:
        response = agent_response(bedrock, final_input)
        if response:
            st.session_state.messages.append(("Agent", response))
        else:
            st.session_state.messages.append(("Agent", "Sorry, I couldn't generate a response. Please try again."))
    except Exception as e:
        error_str = str(e)
        if "AccessDeniedException" in error_str or "not authorized" in error_str:
            fallback_response = "Demo mode activated: I'm running with sample responses due to AWS permissions. Your question: " + final_input
        else:
            fallback_response = f"Error: {error_str}"
        st.session_state.messages.append(("Agent", fallback_response))
    
    typing_placeholder.empty()
    st.rerun()

# Chat display area
st.markdown("---")

if st.session_state.messages:
    for idx, message in enumerate(st.session_state.messages):
        role, msg = message
        if role == "You":
            with st.chat_message("user"):
                st.markdown(msg)
        else:
            with st.chat_message("assistant"):
                st.markdown(msg)
                
                # Rating buttons for agent responses
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("👍", key=f"up_{idx}"):
                        st.session_state.ratings[idx] = "helpful"
                        st.success("Thanks for the feedback!")
                with col2:
                    if st.button("👎", key=f"down_{idx}"):
                        st.session_state.ratings[idx] = "not_helpful"
                        st.info("We'll improve this.")
else:
    st.info("👋 Start by asking a question or click a quick reply!")

# Status indicator
if not bedrock_available:
    st.warning("💡 **Demo Mode Active** - Using sample responses. To enable Bedrock, ensure your AWS user has `bedrock:InvokeModel` permission.")
else:
    st.success("✅ **Bedrock Connected** - Using AWS Bedrock for responses")

# Export chat
if st.session_state.get("export_requested"):
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "conversation": st.session_state.messages,
        "ratings": st.session_state.ratings
    }
    
    st.download_button(
        label="📄 Download Chat as JSON",
        data=json.dumps(chat_data, indent=2),
        file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
    st.session_state.export_requested = False
