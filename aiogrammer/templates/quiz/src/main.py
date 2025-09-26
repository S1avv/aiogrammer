import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from src.config import settings
from src.logger import setup_logging
from src.db import init_models, session
from src.repo import get_or_create_user, get_random_question, increment_score, add_question


class AnswerState(StatesGroup):
    waiting_for_answer = State()


async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Welcome to Quiz Bot! Use /quiz to get a question. Use /addq to add a question (admin/demo).")


async def cmd_quiz(message: Message, state: FSMContext):
    async with session() as s:
        user = await get_or_create_user(s, message.from_user.id, message.from_user.username)
        q = await get_random_question(s)
    if not q:
        await message.answer("No questions yet. Use /addq <question> | <answer> to add one.")
        return
    await state.update_data(q_id=q.id, q_text=q.text, answer=q.answer.lower().strip())
    await message.answer(f"Question: {q.text}\nReply with your answer.")
    await state.set_state(AnswerState.waiting_for_answer)


async def on_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    correct = data.get("answer")
    if correct is None:
        await message.answer("Please start a quiz with /quiz")
        return
    user_answer = message.text.lower().strip()
    if user_answer == correct:
        async with session() as s:
            user = await get_or_create_user(s, message.from_user.id, message.from_user.username)
            await increment_score(s, user)
        await message.answer("Correct! +1 point. Use /quiz for another question.")
    else:
        await message.answer(f"Incorrect. Correct answer: {correct}. Use /quiz to try another.")
    await state.clear()


async def cmd_addq(message: Message):
    payload = message.text.split(maxsplit=1)
    if len(payload) < 2 or "|" not in payload[1]:
        await message.answer("Usage: /addq <question> | <answer>")
        return
    text_part, answer_part = map(str.strip, payload[1].split("|", maxsplit=1))
    if not text_part or not answer_part:
        await message.answer("Both question and answer must be non-empty")
        return
    async with session() as s:
        await add_question(s, text_part, answer_part)
    await message.answer("Question added.")


async def main():
    logger = setup_logging()
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    await init_models()

    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_addq, Command("addq"))
    dp.message.register(on_answer, AnswerState.waiting_for_answer, F.text)

    logger.info("Quiz bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())