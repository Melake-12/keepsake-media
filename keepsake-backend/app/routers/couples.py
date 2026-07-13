from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import Couple, User
from app.schemas.schemas import CoupleCreateOut, JoinCoupleIn

router = APIRouter(prefix="/couples", tags=["couples"])


@router.post("", response_model=CoupleCreateOut)
def create_couple(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="You're already paired with someone")

    couple = Couple(name=f"{current_user.display_name}'s couple")
    db.add(couple)
    db.commit()
    db.refresh(couple)

    current_user.couple_id = couple.id
    db.commit()

    return couple


@router.post("/join", response_model=CoupleCreateOut)
def join_couple(
    payload: JoinCoupleIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="You're already paired with someone")

    couple = db.query(Couple).filter(Couple.invite_code == payload.invite_code).first()
    if not couple:
        raise HTTPException(status_code=404, detail="Invite code not found")

    existing_members = db.query(User).filter(User.couple_id == couple.id).count()
    if existing_members >= 2:
        raise HTTPException(status_code=400, detail="This couple already has two people")

    current_user.couple_id = couple.id
    db.commit()

    return couple
