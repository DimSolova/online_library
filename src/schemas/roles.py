from pydantic import BaseModel, ConfigDict


class RoleAddDTO(BaseModel):
    name: str
    description: str


class RoleDTO(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
