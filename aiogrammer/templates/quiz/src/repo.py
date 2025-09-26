from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Question


async def get_or_create_user(session: AsyncSession, tg_id: int, username: Optional[str]) -> User:
    res = await session.execute(select(User).where(User.tg_id == tg_id))
    user = res.scalar_one_or_none()
    if user is None:
        user = User(tg_id=tg_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def add_question(session: AsyncSession, text: str, answer: str) -> Question:
    q = Question(text=text, answer=answer)
    session.add(q)
    await session.commit()
    await session.refresh(q)
    return q


async def get_random_question(session: AsyncSession) -> Optional[Question]:
    res = await session.execute(select(Question).order_by(func.random()).limit(1))
    return res.scalar_one_or_none()


async def increment_score(session: AsyncSession, user: User) -> None:
    user.score += 1
    await session.commit()