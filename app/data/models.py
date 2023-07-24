from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .db import Base



class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu",cascade="all, delete")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",cascade="all, delete")

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")
    