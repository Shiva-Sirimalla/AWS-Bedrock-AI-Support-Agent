# 🚀 AWS Bedrock AI Support Agent

An interactive customer support chatbot powered by AWS Bedrock and Llama 3 8B, built with Streamlit. Features intelligent conversation routing, quick replies, chat analytics, and export functionality.

---

## ✨ Features

### Core Chatbot Capabilities
- **AWS Bedrock Integration** - Uses `meta.llama3-8b-instruct-v1:0` model for intelligent responses
- **FAQ Database** - Quick answers for common questions (refunds, delivery, etc.)
- **Ticket Creation** - Automatically creates support tickets for reported issues
- **Demo Mode** - Works without AWS credentials using sample responses (perfect for testing!)

### User Experience
- **💬 Chat Interface** - Clean, modern chat UI with message bubbles
- **⚡ Quick Reply Buttons** - Pre-built responses for common questions:
  - How long does delivery take?
  - What's your refund policy?
  - I need technical support
  - Can I track my order?
  - How do I cancel?

- **🤖 Typing Indicator** - Shows "Agent is thinking..." while processing
- **👍👎 Response Ratings** - Users can rate if responses were helpful

### Analytics & Export
- **📊 Chat Analytics** - Track conversation metrics:
  - Total messages
  - User messages count
  - Agent responses count
  
- **📥 Export Chat** - Download conversations as JSON with:
  - Full conversation history
  - User ratings for each response
  - Timestamp of export
  
- **🗑️ Clear History** - Reset chat with one click

### Demo Mode
- Graceful fallback when AWS credentials are missing or invalid
- Sample responses for all supported questions
- Clear status indicator showing "Demo Mode Active"
- No errors - just seamless operation

---

## 📋 Architecture

```
agent_bedrock/
├── app.py              # Main Streamlit application
├── agent.py            # Agent logic & Bedrock integration
├── config.py           # AWS client configuration
├── tools.py            # Support tools (FAQ, ticket creation)
└── README.md           # This file
```

### Component Flow
```
User Input
    ↓
[Quick Replies] or [Text Input]
    ↓
Agent Processing
    ↓
├─→ FAQ Lookup (fastest)
├─→ Bedrock Decision Making (if available)
├─→ Bedrock Response Generation (if available)
└─→ Demo Mode Fallback (if needed)
    ↓
Chat Display with Ratings
    ↓
Export Option
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Streamlit
- boto3
- AWS Account with Bedrock access

### 1. Install Dependencies
```bash
pip install streamlit boto3
```

### 2. Run the Application
```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

### 3. Configure AWS Credentials (Optional)
In the sidebar, enter:
- **AWS Access Key** - Your AWS access key ID
- **AWS Secret Key** - Your AWS secret access key

**Note:** Leave credentials blank to use Demo Mode with sample responses!

---

## 📖 Usage Guide

### 1. **Chat Interface**
```
┌─────────────────────────────────────────┐
│ 🚀 AWS Bedrock AI Support Agent         │
│ Powered by AWS Bedrock • Llama 3 8B     │
├─────────────────────────────────────────┤
│                                         │
│ [Ask your question...]  [Send 📤]      │
│                                         │
│ 💡 Quick replies:                       │
│ [Delivery?] [Refund?] [Support] ...    │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│ You: "How long does delivery take?"     │
│                                         │
│ Agent: "Delivery takes 3-5 days."       │
│ 👍 👎                                    │
│                                         │
└─────────────────────────────────────────┘
```

### 2. **Sidebar Controls**
- **AWS Credentials** - Connect to your AWS account
- **Chat Analytics** - View conversation metrics
- **Export Chat** - Download as JSON
- **Clear Chat** - Reset conversation

### 3. **Demo Questions**
Try these to test the chatbot:
- "How long does delivery take?"
- "What's your refund policy?"
- "I have a technical problem"
- "Can I track my order?"
- "How do I cancel my order?"

### 4. **Rating Responses**
After each agent response, click:
- 👍 if the response was helpful
- 👎 if it needs improvement

Ratings are tracked and exported with your chat history.

---

## 🔐 AWS Permissions Required

To use Bedrock integration, your AWS user needs this IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:ListFoundationModels"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/chat_memory"
    }
  ]
}
```

### Troubleshooting Permission Issues
If you see: `AccessDeniedException: User is not authorized to perform bedrock:InvokeModel`

**Solution:** The app automatically falls back to Demo Mode! No action needed - it will work with sample responses.

---

## 📤 Export Format

When you export a chat, you get a JSON file with this structure:

```json
{
  "timestamp": "2026-07-10T00:56:30.123456",
  "conversation": [
    ["You", "How long does delivery take?"],
    ["Agent", "Delivery takes 3-5 days."],
    ["You", "What about refunds?"],
    ["Agent", "Refunds take 5-7 business days."]
  ],
  "ratings": {
    "1": "helpful",
    "3": "not_helpful"
  }
}
```

---

## 🎯 Core Files Explained

### `app.py` - Main Application
- Streamlit UI with chat interface
- Sidebar controls and analytics
- Quick reply button handling
- Message processing and display
- Export functionality
- Error handling and Demo Mode fallback

### `agent.py` - Agent Logic
```python
agent_response(client, user_input)
  ├─→ FAQ Lookup (tools.get_faq_answer)
  ├─→ Bedrock Decision Making (invoke_bedrock)
  ├─→ Ticket Creation (tools.create_ticket)
  └─→ Bedrock Response Generation (invoke_bedrock)
```

### `config.py` - AWS Configuration
- Bedrock client initialization
- DynamoDB client initialization
- Uses AWS credentials from sidebar

### `tools.py` - Support Functions
- `create_ticket()` - Creates support tickets
- `get_faq_answer()` - FAQ lookup engine

---

## 🚀 Advanced Features

### 1. **Multi-turn Conversations**
Chat history is maintained in session state. Clear chat to start fresh.

### 2. **Sentiment-Aware Routing**
The agent uses decision prompts to determine if issues need ticket creation.

### 3. **Graceful Degradation**
Works in three modes:
- ✅ **Full Bedrock Mode** - AWS credentials + permissions valid
- ⚠️ **Partial Mode** - AWS connected but permission denied → auto-fallback
- 💡 **Demo Mode** - No credentials provided → uses sample responses

### 4. **Analytics Tracking**
Session-based metrics:
- Message count
- Response ratings
- Export with timestamps

---

## 🔧 Customization

### Add More Quick Replies
Edit `app.py` line ~11:
```python
QUICK_REPLIES = [
    "Your new question here",
    # ... more replies
]
```

### Add More FAQ Answers
Edit `tools.py`:
```python
faq = {
    "your_keyword": "Your answer here",
    # ... more FAQ items
}
```

### Change the Model
Edit `agent.py` line ~5:
```python
MODEL_ID = "meta.llama3-70b-instruct-v1:0"  # Different model
```

---

## 📊 Session Analytics Example

```
📊 Chat Analytics
Total Messages: 8
User Messages: 4
Agent Responses: 4

Ratings Summary:
✅ Helpful: 2
❌ Not Helpful: 1
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "AccessDeniedException" | Demo Mode activates automatically. Add IAM permissions to use Bedrock. |
| No response from agent | Check AWS credentials in sidebar or use Demo Mode. |
| Quick replies not working | Refresh the page. Try typing in the text input instead. |
| Export button not visible | Send at least one message first. |
| Chat not clearing | Try the 🗑️ button in the sidebar. |

---

## 📝 Environment Variables (Optional)

```bash
# Set AWS region (default: us-east-1)
AWS_REGION=us-east-1

# Set Bedrock model
BEDROCK_MODEL=meta.llama3-8b-instruct-v1:0
```

---

## 🎓 Example Interactions

### Example 1: FAQ Response
```
User: "How long does delivery take?"
↓
Agent (FAQ Match): "Delivery takes 3-5 days."
```

### Example 2: Support Ticket
```
User: "My order is broken"
↓
Agent (Decision): "Ticket created for issue: My order is broken"
```

### Example 3: General Query
```
User: "Do you have a warranty?"
↓
Agent (Bedrock): [Generates intelligent response]
```

---

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | latest | Web UI framework |
| boto3 | latest | AWS SDK for Python |
| python | 3.8+ | Runtime |

Install all:
```bash
pip install streamlit boto3
```

---

## 🎨 UI Components

```
┌─ HEADER ─────────────────────────────────────┐
│ 🚀 AWS Bedrock AI Support Agent              │
│ Powered by AWS Bedrock • Llama 3 8B Instruct │
└──────────────────────────────────────────────┘

┌─ SIDEBAR ────────────────┐
│ ⚙️ Configuration         │
│ AWS Access Key: [****]   │
│ AWS Secret Key: [****]   │
│                          │
│ 📊 Chat Analytics        │
│ Total: 5                 │
│ User: 3                  │
│ Agent: 2                 │
│                          │
│ [📥 Export] [🗑️ Clear]   │
└──────────────────────────┘

┌─ INPUT AREA ─────────────────────────────────┐
│ [Ask your question...]        [Send 📤]      │
│                                              │
│ 💡 Quick replies:                            │
│ [Delivery?] [Refund?] [Support] [Track] ...  │
└──────────────────────────────────────────────┘

┌─ CHAT AREA ──────────────────────────────────┐
│                                              │
│ YOU: "How long does delivery take?"          │
│ ┌──────────────────────────────────────────┐ │
│ │ Agent: "Delivery takes 3-5 days."        │ │
│ │ 👍 👎                                     │ │
│ └──────────────────────────────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘

┌─ STATUS ─────────────────────────────────────┐
│ 💡 Demo Mode Active                          │
│ Using sample responses                       │
└──────────────────────────────────────────────┘
```

---

## 🚀 Performance Tips

1. **First Load** - May take 5-10 seconds to initialize Streamlit
2. **Bedrock Calls** - Usually respond in 2-3 seconds
3. **Demo Mode** - Instant responses (< 100ms)
4. **Export** - Fast JSON generation (< 1 second)

---

## 📦 Project Size & Scope

- **Total Files**: 4 Python files + 1 README
- **Lines of Code**: ~200 (app.py) + ~40 (agent.py) + ~20 (config.py) + ~15 (tools.py)
- **Dependencies**: 2 core packages (streamlit, boto3)
- **Setup Time**: < 2 minutes

---

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install streamlit boto3`
2. ✅ Run the app: `streamlit run app.py`
3. ✅ Try Demo Mode (no credentials needed!)
4. ✅ Add AWS credentials to enable Bedrock
5. ✅ Export and analyze conversations

---

## 📞 Support

- **Demo Mode Not Working?** - Refresh the page
- **Bedrock Connection Issues?** - Check IAM permissions
- **Chat Not Displaying?** - Clear browser cache and refresh
- **Export Not Showing?** - Send at least one message first

---

## 📜 License

This project is part of the AWS Bedrock AI Support Agent initiative.

---

**Built with ❤️ using AWS Bedrock, Llama 3, and Streamlit**

