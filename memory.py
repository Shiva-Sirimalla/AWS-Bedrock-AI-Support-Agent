def save_message(table, session_id, role, message):
    table.put_item(Item={
        "session_id": session_id,
        "role": role,
        "message": message
    })

def get_history(table, session_id):
    response = table.query(
        KeyConditionExpression="session_id = :sid",
        ExpressionAttributeValues={":sid": session_id}
    )
    return response.get("Items", [])
