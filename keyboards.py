from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Родитель'),
                                KeyboardButton(text='Учитель')]],
                           resize_keyboard=True,
                           input_field_placeholder='Кто вы?')


teacher = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить родителя'),
                                KeyboardButton(text='Добавить оценки'),
                                         KeyboardButton(text='Выход')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите что вы хотите')

subjects = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Математика'),
                                KeyboardButton(text='Русский язык'),
                                KeyboardButton(text='Литература'),
                                KeyboardButton(text='История'),
                                          KeyboardButton(text='Выход')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите предмет')

