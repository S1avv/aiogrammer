from aiogram.fsm.state import State, StatesGroup

class TicketForm(StatesGroup):
    topic = State()
    description = State()