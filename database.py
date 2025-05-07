import json

def get_phrasal_verbs():
    with open('phrasal_verbs_grouped.json', 'r') as f:
        data = json.load(f)
    return data
