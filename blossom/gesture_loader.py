import json

def load_config(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def getGesture(config, index):
    key = str(index)
    return config.get(key, "Key not found")
