from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class LeadForm(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()

@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Привет! Для начала работы используйте ссылку от менеджера."
        )
        return

    invite_token = args[1]
    await state.update_data(invite_token=invite_token)
    await state.set_state(LeadForm.waiting_name)
    await message.answer("Привет! Как вас зовут?")
