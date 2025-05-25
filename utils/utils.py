import re

def preprocess(message):
    """ Remove punctuation, cast to lower case and split the message """
    cleaned_message = re.sub(r'\W+', ' ', message.lower())
    return set(cleaned_message.split())
