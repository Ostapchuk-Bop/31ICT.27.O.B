import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models import User, Category, Post, Comment, Tag, UserProfile
from app.db.base import Base


async def seed_data():
    async with AsyncSessionLocal() as session:
        from sqlalchemy import delete
        # Clear existing data to avoid UniqueViolation errors
        await session.execute(delete(Comment))
        await session.execute(delete(Post))
        await session.execute(delete(UserProfile))
        await session.execute(delete(User))
        await session.execute(delete(Category))
        await session.execute(delete(Tag))
        await session.commit()

        # Create users
        user1 = User(username="john_doe", email="john@example.com", hashed_password="password1", is_active=True)
        user2 = User(username="jane_smith", email="jane@example.com", hashed_password="password2", is_active=True)
        session.add(user1)
        session.add(user2)
        await session.commit()

        # Create categories
        cat1 = Category(name="Technology", description="Tech related posts")
        cat2 = Category(name="Science", description="Science related posts")
        session.add(cat1)
        session.add(cat2)
        await session.commit()

        # Create posts
        post1 = Post(title="FastAPI Tutorial", content="Learn FastAPI", published=True, author_id=user1.id, category_id=cat1.id)
        post2 = Post(title="Quantum Physics", content="Basics of quantum", published=False, author_id=user2.id, category_id=cat2.id)
        session.add(post1)
        session.add(post2)
        await session.commit()

        # Create comments
        comment1 = Comment(content="Great tutorial!", author_id=user2.id, post_id=post1.id)
        comment2 = Comment(content="Very informative", author_id=user1.id, post_id=post2.id)
        session.add(comment1)
        session.add(comment2)
        await session.commit()

        # Create tags
        tag1 = Tag(name="Python")
        tag2 = Tag(name="Web Development")
        tag3 = Tag(name="Physics")
        session.add(tag1)
        session.add(tag2)
        session.add(tag3)
        await session.commit()

        # Create profiles
        profile1 = UserProfile(full_name="John Doe", bio="Developer from NY", user_id=user1.id)
        profile2 = UserProfile(full_name="Jane Smith", bio="Scientist from London", user_id=user2.id)
        session.add(profile1)
        session.add(profile2)
        await session.commit()

        print("Seed data added successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())