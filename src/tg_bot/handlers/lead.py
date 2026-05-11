from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.tg_bot.services.lead_service import create_lead
from src.tg_bot.handlers.start import LeadForm
from src.tg_bot.keyboards.reply import phone_request_keyboard, remove_keyboard

router = Router()

@router.message(LeadForm.waiting_name, F.text)
async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(LeadForm.waiting_phone)
    await message.answer(
        "Введите ваш номер телефона:",
        reply_markup=phone_request_keyboard()  # показываем кнопку
    )


@router.message(LeadForm.waiting_phone, F.contact)  # F.contact — юзер нажал кнопку
async def handle_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number  # верифицированный номер
    await _process_phone(message, state, phone)


@router.message(LeadForm.waiting_phone, F.text)  # юзер ввёл вручную
async def handle_phone_text(message: Message, state: FSMContext):
    await _process_phone(message, state, message.text)


async def _process_phone(message: Message, state: FSMContext, phone: str):
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.waiting_email)
    await message.answer(
        "Введите ваш email:",
        reply_markup=remove_keyboard()  # убираем клавиатуру
    )


@router.message(LeadForm.waiting_email, F.text)
async def handle_email(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    result = await create_lead(
        invite_token=data["invite_token"],
        name=data["name"],
        phone=data["phone"],
        email=message.text,
        telegram_id=message.from_user.id,
    )
    if result:
        await message.answer(
            f"Спасибо, {data['name']}! Ваша заявка принята. Менеджер свяжется с вами.",
            reply_markup=remove_keyboard()
        )
    else:
        await message.answer(
            "Что-то пошло не так. Попробуйте снова — напишите /start",
            reply_markup=remove_keyboard()
        )
