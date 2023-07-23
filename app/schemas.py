from pydantic import BaseModel, ConfigDict
import uuid


class MenuBase(BaseModel):
    title: str 
    description : str | None = None

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
    id: uuid.UUID
    submenus_count : int = 0
    dishes_count : int = 0



class SubMenuBase(BaseModel):
    title: str 
    description : str | None = None

class SubMenuCreate(SubMenuBase):
    pass

class SubMenu(SubMenuBase):
    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
    id:uuid.UUID
    menu_id : uuid.UUID
    dishes_count : int = 0

class DishBase(BaseModel):
    title: str
    description : str | None = None
    price: str


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
    id: uuid.UUID
    submenu_id: uuid.UUID
