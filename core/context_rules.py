def decide_action(context):
    if context == "public":
        return "blur"
    elif context == "private":
        return "erase"
    else:
        return None
    