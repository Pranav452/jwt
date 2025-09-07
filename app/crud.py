from sqlalchemy.orm import Session
from app.models import User, Groups
from app.schemas import UserCreate, GroupsCreate, ExpensesCreate
from app.auth.hashing import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
    
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw, username=user.username, created_at=user.created_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_group(db: Session, group: GroupsCreate):
    db_group = Groups(name=group.name, created_by=group.created_by, members=group.members, created_at=group.created_at)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups_by_user(db: Session, user_id: int):
    """
    Returns a list of groups the user is a member of.
    """
    return db.query(Groups).filter(Groups.members.contains([user_id])).all()

def get_group_by_id(db: Session, group_id: int):
    """
    Returns the group details for the given group_id.
    """
    return db.query(Groups).filter(Groups.id == group_id).first()

def add_member_to_group(db: Session, group_id: int, user_id: int):
    """
    Adds a new member (user_id) to the group (group_id).
    """
    group = db.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        return None
    # Ensure members is a list; handle both int and list for backward compatibility
    if isinstance(group.members, int):
        members = [group.members]
    else:
        members = group.members if group.members else []
    if user_id not in members:
        members.append(user_id)
        group.members = members
        db.commit()
        db.refresh(group)
    return group

def create_expense_for_group(db: Session, group_id: int, expense_data):
    """
    Creates a new expense for a specific group.
    Expects: amount, description, paid_by, split_between
    """
    from .models import Expense  # Assuming Expense model exists
    expense = Expense(
        group_id=group_id,
        amount=expense_data.amount,
        description=expense_data.description,
        paid_by=expense_data.paid_by,
        split_between=expense_data.split_between,
        created_at=expense_data.created_at
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses_by_group_id(db: Session, group_id: int):
    """
    Returns a list of all expenses for the specified group.
    """
    from .models import Expense  # Assuming Expense model exists
    return db.query(Expense).filter(Expense.group_id == group_id).all()
