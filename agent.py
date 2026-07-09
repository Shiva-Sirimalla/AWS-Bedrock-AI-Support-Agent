import json
from tools import create_ticket, get_faq_answer

# ✅ Llama model
MODEL_ID = "meta.llama3-8b-instruct-v1:0"

# Simple responses for demo/fallback
DEMO_RESPONSES = {
    "help": "I can help you with refunds, delivery, billing, and technical issues. What's your concern?",
    "refund": "Refunds take 5-7 business days. Check your email for confirmation.",
    "delivery": "Most orders arrive in 3-5 business days. You can track your order using the link in your email.",
    "ticket": "A support ticket has been created. Our team will respond within 24 hours.",
    "default": "Thank you for your question. I'm here to help! Please provide more details so I can assist you better."
}

def invoke_bedrock(client, prompt):
    body = json.dumps({
        "prompt": prompt,
        "max_gen_len": 300,
        "temperature": 0.5
    })

    try:
        response = client.invoke_model(
            modelId=MODEL_ID,
            body=body
        )

        result = json.loads(response['body'].read())

        # ✅ Handle multiple formats
        if "generation" in result:
            return result["generation"]

        elif "outputs" in result:
            return result["outputs"][0]["text"]

        else:
            return None

    except Exception as e:
        return None


def agent_response(client, user_input):
    
    # ✅ Step 1: FAQ shortcut
    faq = get_faq_answer(user_input)
    if faq:
        return faq

    # ✅ Step 2: Try Bedrock (if available)
    if client:
        try:
            decision_prompt = f"""
You are a customer support AI agent.

User Query: {user_input}

Rules:
- If user reports a problem → respond ONLY with CREATE_TICKET
- Otherwise → respond normally

Response:
"""
            
            decision = invoke_bedrock(client, decision_prompt)
            
            if decision and "CREATE_TICKET" in decision:
                return create_ticket(user_input)
            
            # Try to get response from Bedrock
            final_response = invoke_bedrock(client, user_input)
            
            if final_response and final_response.strip():
                return final_response
        except:
            pass
    
    # ✅ Step 3: Fallback demo responses
    user_lower = user_input.lower()
    for key, response in DEMO_RESPONSES.items():
        if key != "default" and key in user_lower:
            return response
    
    return DEMO_RESPONSES["default"]