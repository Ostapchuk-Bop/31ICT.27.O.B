from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_post
from app.db.session import get_db
from app.schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
async def read_posts(db: AsyncSession = Depends(get_db)):
    return await crud_post.list_posts(db)

@router.get("/{post_id}", response_model=PostResponse)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post

@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(payload: PostCreate, db: AsyncSession = Depends(get_db)):
    return await crud_post.create_post(db, payload)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, payload: PostUpdate, db: AsyncSession = Depends(get_db)):
    post = await crud_post.update_post(db, post_id, payload)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post

@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_post.delete_post(db, post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return None