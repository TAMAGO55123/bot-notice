import json
file_path = "status.json"
try:
    with open(file_path, mode="x") as f:
        json.dump({}, f)
except FileExistsError:
    pass
def get_status(id:int):
    _id = str(id)
    with open(file_path, mode="r") as f:
        data = json.load(f)
    if _id not in data:
        return None
    return data[_id]
def set_status(id:int, status:str):
    _id = str(id)
    with open(file_path, mode="r") as f:
        data = json.load(f)
    data[_id] = status
    with open(file_path, mode="w") as f:
        json.dump(data, f, indent=4)
