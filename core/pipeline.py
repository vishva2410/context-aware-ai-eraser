from core.context_rules import decide_action
def process_image(image, context, selection):
    action = decide_action(context)
    return image
