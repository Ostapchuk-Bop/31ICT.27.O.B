from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_comment
from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter()

@router.get("/", response_model=List[CommentResponse])
async def read_comments(db: AsyncSession = Depends(get_db)):
    return await crud_comment.list_comments(db)

@router.get("/{comment_id}", response_model=CommentResponse)
async def read_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud_comment.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    return comment

@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(payload: CommentCreate, db: AsyncSession = Depends(get_db)):
    return await crud_comment.create_comment(db, payload)

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, payload: CommentUpdate, db: AsyncSession = Depends(get_db)):
    comment = await crud_comment.update_comment(db, comment_id, payload)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    return comment

@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_comment.delete_comment(db, comment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    return None