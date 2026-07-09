def create_ticket(user_query):
    return f"Ticket created for issue: {user_query}"

def get_faq_answer(query):
    faq = {
        "refund": "Refunds take 5-7 business days.",
        "delivery": "Delivery takes 3-5 days."
    }

    for key in faq:
        if key in query.lower():
            return faq[key]

    return None
