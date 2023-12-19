def get_response_message(data, model, action="create"):
    obj_response_message = data.get("response_message", None)
    response_message = f"{obj_response_message} {action}d successfully"
    return response_message


def remove_null_key_value_pair(dictionary):
    return {k: v for k, v in dictionary.items() if v not in [None, "", "N/A"]}

