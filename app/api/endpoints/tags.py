from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_tag
from app.db.session import get_db
from app.schemas.tag import TagCreate, TagResponse, TagUpdate

router = APIRouter()

@router.get("/", response_model=List[TagResponse])
async def read_tags(db: AsyncSession = Depends(get_db)):
    return await crud_tag.list_tags(db)

@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await crud_tag.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag

@router.post("/", response_model=TagResponse, status_code=201)
async def create_tag(payload: TagCreate, db: AsyncSession = Depends(get_db)):
    return await crud_tag.create_tag(db, payload)

@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, payload: TagUpdate, db: AsyncSession = Depends(get_db)):
    tag = await crud_tag.update_tag(db, tag_id, payload)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag

@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_tag.delete_tag(db, tag_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return None