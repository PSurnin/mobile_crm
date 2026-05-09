from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

def phone_request_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поделиться номером", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # скроется после нажатия
    )

def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
