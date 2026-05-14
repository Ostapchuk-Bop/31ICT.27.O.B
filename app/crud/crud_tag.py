from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


async def list_tags(db: AsyncSession) -> List[Tag]:
    result = await db.execute(select(Tag))
    return result.scalars().all()


async def get_tag(db: AsyncSession, tag_id: int) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalar_one_or_none()


async def create_tag(db: AsyncSession, payload: TagCreate) -> Tag:
    tag = Tag(
        name=payload.name,
    )
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(db: AsyncSession, tag_id: int, payload: TagUpdate) -> Tag | None:
    tag = await get_tag(db, tag_id)
    if not tag:
        return None

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(tag, key, value)

    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(db: AsyncSession, tag_id: int) -> bool:
    tag = await get_tag(db, tag_id)
    if not tag:
        return False

    await db.delete(tag)
    await db.commit()
    return True