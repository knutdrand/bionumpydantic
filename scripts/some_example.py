from pydantic import BaseModel

class OurModel(BaseModel):
    name: str
    scores: list[int]

#OurModel(name="test", scores=['1', '2.1', 3])
