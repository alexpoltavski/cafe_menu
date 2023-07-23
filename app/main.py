from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uuid

from . import crud, models, schemas
from .db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Menu endpoints
@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = crud.get_menus(db, skip=skip,limit=limit)
    return menus

@app.post("/api/v1/menus", response_model=schemas.Menu,status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)

@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    db_menu =crud.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus_count = crud.get_menu_submenus_count(db=db,menu_id=menu_id)
    dishes_count = crud.get_menu_dishes_count(db=db,menu_id=menu_id)
    return schemas.Menu(title=db_menu.title, description=db_menu.description, id=db_menu.id, submenus_count=submenus_count, dishes_count=dishes_count)
    
@app.patch("/api/v1/menus/{menu_id}")
def update_menu(menu_id: uuid.UUID, menu: schemas.MenuCreate,db: Session = Depends(get_db)):
    return crud.update_menu(db=db, menu_id=menu_id, menu=menu)

@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.delete_menu(db=db, menu_id=menu_id)


# Submenu endpoints
@app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubMenu])
def read_submenus(menu_id: uuid.UUID,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_submenus = crud.get_submenus(db, menu_id=menu_id, skip=skip,limit=limit)
    submenus=[]
    for i in db_submenus:
        dishes_count = crud.get_submenu_dishes_count(db=db, submenu_id=i.id)
        submenus.append(schemas.SubMenu(title=i.title, description=i.description, id=i.id,menu_id=i.menu_id,dishes_count=dishes_count))
    return submenus

@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubMenu,status_code=201)
def create_submenu(menu_id: uuid.UUID,submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    return crud.create_submenu(db=db, submenu=submenu, menu_id=menu_id)

@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def read_submenu(submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db=db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    dishes_count = crud.get_submenu_dishes_count(db=db, submenu_id=submenu_id)
    return schemas.SubMenu(title=db_submenu.title, description=db_submenu.description, id=db_submenu.id, menu_id=db_submenu.menu_id,dishes_count=dishes_count)

@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def update_submenu(submenu_id: uuid.UUID, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    return crud.update_submenu(db=db, submenu_id=submenu_id, submenu=submenu)

@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.delete_submenu(db=db, submenu_id=submenu_id)

# Dishes endpoints
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def read_dishes(submenu_id: uuid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = crud.get_dishes(db, submenu_id=submenu_id, skip=skip,limit=limit)
    return dishes

@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish,status_code=201)
def create_dish(dish: schemas.DishCreate, submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.create_dish(db=db, dish=dish, submenu_id=submenu_id)

@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def read_dish(dish_id: uuid.UUID,  db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db=db, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish

@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def update_dish(dish: schemas.DishCreate, dish_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.update_dish(db=db, dish=dish, dish_id=dish_id)

@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.delete_dish(db=db, dish_id=dish_id)