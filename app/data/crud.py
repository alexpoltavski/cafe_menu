from sqlalchemy.orm import Session
import uuid

from . import models, schemas


def get_menu(db: Session, menu_id: uuid.UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Menu).offset(skip).limit(limit).all()

def get_menu_submenus_count(db: Session, menu_id: uuid.UUID):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).count()

def get_menu_dishes_count(db: Session, menu_id: uuid.UUID):
    return db.query(models.Menu).join(models.Menu.submenus).join(models.Submenu.dishes).filter(models.Menu.id == menu_id).count()

def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: uuid.UUID,menu: schemas.MenuBase):
    db_menu = db.get(models.Menu,menu_id)
    db_menu.description = menu.description
    db_menu.title = menu.title
    db.commit()
    db.refresh(db_menu)
    return db_menu
  

def delete_menu(db: Session, menu_id: uuid.UUID):
    db.delete(db.get(models.Menu,menu_id))
    db.commit()


def get_submenu(db: Session, submenu_id: uuid.UUID):
    return db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()

def get_submenus(db: Session, menu_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).offset(skip).limit(limit).all()

def get_submenu_dishes_count(db: Session, submenu_id: uuid.UUID):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).count()

def create_submenu(db: Session, submenu: schemas.SubMenuCreate, menu_id: uuid.UUID):
    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

def update_submenu(db: Session, submenu_id: uuid.UUID,submenu: schemas.SubMenuCreate):
    db_submenu = db.get(models.Submenu,submenu_id)
    db_submenu.description = submenu.description
    db_submenu.title = submenu.title
    db.commit()
    db.refresh(db_submenu)
    return db_submenu
   
def delete_submenu(db: Session, submenu_id: uuid.UUID):
    db.delete(db.get(models.Submenu,submenu_id))
    db.commit()


def get_dish(db: Session, dish_id: uuid.UUID):
    return db.query(models.Dish).filter(models.Dish.id == dish_id).first()

def get_dishes(db: Session, submenu_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).offset(skip).limit(limit).all()


def create_dish(db: Session, dish: schemas.DishCreate, submenu_id: uuid.UUID):
    db_dish = models.Dish(title=dish.title, description=dish.description, price = dish.price, submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

def update_dish(db: Session, dish_id: uuid.UUID,dish: schemas.DishCreate):
    db_dish = db.get(models.Dish,dish_id)
    db_dish.description = dish.description
    db_dish.title = dish.title
    db_dish.price = dish.price
    db.commit()
    db.refresh(db_dish)
    return db_dish
   

def delete_dish(db: Session, dish_id: uuid.UUID):
    db.delete(db.get(models.Dish,dish_id))
    db.commit()