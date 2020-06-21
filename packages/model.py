import json

def load(root, name):
    path = root / "ressources" / "models" / name
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def load_all(root):
    path = root / "ressources" / "models"
    model_dict = {}
    for file in path.iterdir():
        model = load(file)
        model_dict.update({model["blocknum"]: model})
    return model_dict
