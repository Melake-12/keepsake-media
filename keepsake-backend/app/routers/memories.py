import uuid

import boto3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import Memory, User
from app.schemas.schemas import MemoryOut, MemoryCreateIn

router = APIRouter(prefix="/memories", tags=["memories"])


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key_id,
        aws_secret_access_key=settings.r2_secret_access_key,
        region_name="auto",
    )


@router.get("/upload-url")
def get_upload_url(filename: str, current_user: User = Depends(get_current_user)):
    """Returns a presigned URL the app can PUT the file to directly, keeping
    the file bytes off our own server entirely."""
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="Pair with your partner first")

    object_key = f"{current_user.couple_id}/{uuid.uuid4().hex}-{filename}"
    client = get_r2_client()
    upload_url = client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.r2_bucket_name, "Key": object_key},
        ExpiresIn=600,
    )
    return {"upload_url": upload_url, "object_key": object_key}


@router.post("", response_model=MemoryOut)
def create_memory(
    payload: MemoryCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="Pair with your partner first")

    memory = Memory(
        couple_id=current_user.couple_id,
        uploaded_by=current_user.id,
        r2_object_key=payload.r2_object_key,
        media_type=payload.media_type,
        caption=payload.caption,
        taken_at=payload.taken_at,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


@router.get("", response_model=list[MemoryOut])
def list_memories(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if not current_user.couple_id:
        raise HTTPException(status_code=400, detail="Pair with your partner first")

    return (
        db.query(Memory)
        .filter(Memory.couple_id == current_user.couple_id)
        .order_by(Memory.taken_at.desc().nullslast(), Memory.created_at.desc())
        .all()
    )
