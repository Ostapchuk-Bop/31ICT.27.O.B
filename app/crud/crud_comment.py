from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


async def list_comments(db: AsyncSession) -> List[Comment]:
    result = await db.execute(select(Comment))
    return result.scalars().all()


async def get_comment(db: AsyncSession, comment_id: int) -> Comment | None:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def create_comment(db: AsyncSession, payload: CommentCreate) -> Comment:
    comment = Comment(
        content=payload.content,
        author_id=payload.author_id,
        post_id=payload.post_id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(db: AsyncSession, comment_id: int, payload: CommentUpdate) -> Comment | None:
    comment = await get_comment(db, comment_id)
    if not comment:
        return None

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(comment, key, value)

    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    comment = await get_comment(db, comment_id)
    if not comment:
        return False

    await db.delete(comment)
    await db.commit()
    return True