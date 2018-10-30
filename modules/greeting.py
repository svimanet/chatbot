import random

def greet(user_input):
    """ Responds and greets users. """
    first_word = user_input.split(" ")[0].strip('?!.,;:\n\t\r')
    user_input = user_input.strip('?!.,:;\n\t\r')
    greetings = ['hola', 'hello', 'hi', 'hey!', 'hey', 'halla', 'yo', 'hai', 'hei']
    question = ['whats up', 'sup', 'skjer', 'skjera']
    responses = ['Chillin\'',"Havin a blast", "Ins dd?", "Not doing much."]

    if first_word in greetings:
        print(" IN GREET LIST YES YES")
        random_greeting = random.choice(greetings)
        return random_greeting.title()

    elif user_input in question:
        random_response = random.choice(responses)
        return random_response.title()

    else: return False
