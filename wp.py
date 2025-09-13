import json
from pydantic import BaseModel
from typing_extensions import TypedDict
from dataclasses import dataclass, asdict

#MaseModel
class User(BaseModel):
    name: str
    id: int   
    
user = User(name="Bano", id=17)
agent_output_basemodel = {
    "response": user.model_dump()  #gets wrapped
}
print("BaseModel Output:", json.dumps(agent_output_basemodel, indent=2))
#TypedDict
class Profile(TypedDict):
    city: str
    nic: str

profile: Profile = {"city": "Karachi", "nic": "42201-0545295-6"}
agent_output_typeddict = {
    "response": profile   # gets wrapped
}
print("\nTypedDict Output:", json.dumps(agent_output_typeddict, indent=2))

#dataclasses
@dataclass
class ClassInfo:
    class_level: str
    teacher_name: str

class_info = ClassInfo("Math", 5)

agent_output_dataclass = {
    "response": asdict(class_info)   # gets wrapped
}
print("\nDataclass Output:", json.dumps(agent_output_dataclass, indent=2))

#List[str]
subjects = ["Math", "Biology", "Computer"]
agent_output_list = subjects   # NOT wrapped
print("\nList[str] Output:", json.dumps(agent_output_list, indent=2))