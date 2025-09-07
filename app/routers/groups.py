from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import GroupsCreate, GroupsOut
from app import crud
from app.db import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"], dependencies=[Depends(get_current_user)])

@router.post("/create", response_model=GroupsOut)
def create_group(group: GroupsCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@router.get("/{group_id}", response_model=GroupsOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    return crud.get_group_by_id(db, group_id)

@router.get("/user/{user_id}", response_model=List[GroupsOut])
def get_groups_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_groups_by_user(db, user_id)

@router.post("/{group_id}/add_member", response_model=GroupsOut)
def add_member_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.add_member_to_group(db, group_id, user_id)