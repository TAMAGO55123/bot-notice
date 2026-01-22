import json
from pydantic import BaseModel
class Channels(BaseModel):
    id:int
    name: str

file_path = "presence.json"
try:
    with open(file_path, mode="x") as f:
        json.dump({}, f)
except FileExistsError:
    pass
def get_channel(id:int) -> Channels:
    _id = str(id)
    with open(file_path, mode="r") as f:
        data = json.load(f)
    if _id not in data:
        return None
    return Channels(id=data[_id]["id"], name=data[_id]["name"])
def set_channel(id:int, channels: Channels) ->None:
    _id = str(id)
    with open(file_path, mode="r") as f:
        data = json.load(f)
    data[_id] = {"id": channels.id, "name": channels.name}
    with open(file_path, mode="w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
