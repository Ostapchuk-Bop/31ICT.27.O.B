from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


async def list_posts(db: AsyncSession) -> List[Post]:
    result = await db.execute(select(Post))
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def create_post(db: AsyncSession, payload: PostCreate) -> Post:
    post = Post(
        title=payload.title,
        content=payload.content,
        published=payload.published,
        author_id=payload.author_id,
        category_id=payload.category_id,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def update_post(db: AsyncSession, post_id: int, payload: PostUpdate) -> Post | None:
    post = await get_post(db, post_id)
    if not post:
        return None

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    post = await get_post(db, post_id)
    if not post:
        return False

    await db.delete(post)
    await db.commit()
    return True