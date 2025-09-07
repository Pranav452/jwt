from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ExpensesCreate, ExpensesOut
from app import crud
from app.db import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"], dependencies=[Depends(get_current_user)])

@router.post("/create", response_model=ExpensesOut)
def create_expense(expense: ExpensesCreate, db: Session = Depends(get_db)):
    return crud.create_expense_for_group(db, expense.group_id, expense)

@router.get("/{group_id}", response_model=List[ExpensesOut])
def get_expenses(group_id: int, db: Session = Depends(get_db)):
    return crud.get_expenses_by_group_id(db, group_id)