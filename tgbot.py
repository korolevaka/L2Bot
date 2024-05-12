from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import StateFilter
from aiogram.filters import CommandStart
from sqlalchemy import func
import asyncio

from database import Session, Parent, Grades
import keyboards as kb
import config
from states import Authentication, AddParent, AddGrades, TeacherCode, GetGrades

# Создаем объекты бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def cmd_start(message: Message):
   await message.answer("Добро пожаловать в чат-бот для просмотра успеваемости своего ребёнка!🏫\nВы 👔учитель или 👨‍👩‍👦родитель?", reply_markup=kb.main)

@dp.message(lambda message: message.text == "Учитель")
async def cmd_code(message: Message, state: FSMContext):
    await message.answer("Ввеедите код учителя🤫")
    await state.set_state(TeacherCode.waiting_code)

@dp.message(StateFilter(TeacherCode.waiting_code))
async def process_code(message: Message, state: FSMContext):
    if message.text == config.TEACHER_CODE:
        await message.answer("Что вы хотите сделать?✍🏻", reply_markup=kb.teacher)
        await state.clear()  # Очищаем состояние, чтобы код можно было ввести снова
    else:
        await message.answer("✖️Код не верный. Попробуйте ещё раз.")

@dp.message(lambda message: message.text == "Добавить родителя")
async def add_parent_start(message: Message, state: FSMContext):
    await message.answer("Введите ФИО родителя:")
    await state.set_state(AddParent.waiting_for_parent_name)

@dp.message(StateFilter(AddParent.waiting_for_parent_name))
async def process_parent_name(message: Message, state: FSMContext):
    await state.update_data(parent_name=message.text)
    await message.answer("Введите имя ученика:")
    await state.set_state(AddParent.waiting_for_student_name)

@dp.message(StateFilter(AddParent.waiting_for_student_name))
async def process_student_name(message: Message, state: FSMContext):
    await state.update_data(student_name=message.text)
    await message.answer("Введите пароль:")
    await state.set_state(AddParent.waiting_for_password)


@dp.message(StateFilter(AddParent.waiting_for_password))
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    session = Session()
    # Получаем последний ID из базы
    last_id = session.query(func.max(Parent.id)).scalar()
    if last_id is None:
        new_id = 1
    else:
        new_id = last_id + 1
    new_parent = Parent(
        id=new_id,
        parent_name=data.get("parent_name"),
        student_name=data.get("student_name"),
        password=data.get("password"),
    )
    session.add(new_parent)
    session.commit()
    session.close()
    await message.answer(f"Родитель успешно добавлен! Индивидуальный номер:'{new_id}'", reply_markup=kb.teacher)
    await state.clear()

@dp.message(lambda message: message.text == "Добавить оценки")
async def add_grades_start(message: Message, state: FSMContext):
    await message.answer("Введите ID родителя:")
    await state.set_state(AddGrades.waiting_for_parent_id)

@dp.message(StateFilter(AddGrades.waiting_for_parent_id))
async def process_parent_id(message: Message, state: FSMContext):
    try:
        parent_id = int(message.text)
        await state.update_data(parent_id=parent_id)
        await message.answer("Введите оценку по математике:")
        await state.set_state(AddGrades.waiting_for_math)
    except ValueError:
        await message.answer("✖️Неверный ID родителя. Введите число.")


@dp.message(StateFilter(AddGrades.waiting_for_math))
async def process_math(message: Message, state: FSMContext):
    try:
        math = int(message.text)
        await state.update_data(math=math)
        await message.answer("Введите оценку по русскому языку:")
        await state.set_state(AddGrades.waiting_for_russian)
    except ValueError:
        await message.answer("✖️Неверная оценка. Введите число.")

@dp.message(StateFilter(AddGrades.waiting_for_russian))
async def process_russian(message: Message, state: FSMContext):
    try:
        russian = int(message.text)
        await state.update_data(russian=russian)
        await message.answer("Введите оценку по истории:")
        await state.set_state(AddGrades.waiting_for_history)
    except ValueError:
        await message.answer("✖️Неверная оценка. Введите число.")

@dp.message(StateFilter(AddGrades.waiting_for_history))
async def process_history(message: Message, state: FSMContext):
    try:
        history = int(message.text)
        await state.update_data(history=history)
        await message.answer("Введите оценку по литературе:")
        await state.set_state(AddGrades.waiting_for_literature)
    except ValueError:
        await message.answer("✖️Неверная оценка. Введите число.")

@dp.message(StateFilter(AddGrades.waiting_for_literature))
async def process_literature(message: Message, state: FSMContext):
    try:
        literature = int(message.text)
        await state.update_data(literature=literature)
        data = await state.get_data()

        session = Session()
        new_grades = Grades(
            parent_id=data.get("parent_id"),
            math=data.get("math"),
            russian=data.get("russian"),
            history=data.get("history"),
            literature=data.get("literature"),
        )
        session.add(new_grades)
        session.commit()
        session.close()
        await message.answer("Оценки успешно добавлены!", reply_markup=kb.teacher)
        await state.clear()
    except ValueError:
        await message.answer("✖️Неверная оценка. Введите число.")

@dp.message(lambda message: message.text == "Родитель")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Здравствуйте!👋🏻\nВведите ваше ФИО:")
    await state.set_state(Authentication.waiting_for_parent_name)

@dp.message(StateFilter(Authentication.waiting_for_parent_name))
async def process_parent_name(message: Message, state: FSMContext):
    parent_name = message.text
    session = Session()
    result = session.query(Parent).filter_by(parent_name=parent_name).first()
    if result:
        await state.update_data(parent_name=parent_name)
        await message.answer("Введите ФИО ребенка:")
        await state.set_state(Authentication.waiting_for_student_name)
    else:
        await message.answer("✖️ФИО введено не верно, попробуйте снова:")

@dp.message(StateFilter(Authentication.waiting_for_student_name))
async def process_student_name(message: Message, state: FSMContext):
    student_name = message.text
    session = Session()
    result = session.query(Parent).filter_by(student_name=student_name).first()
    if result:
        await state.update_data(student_name=message.text)
        await message.answer("Введите пароль:")
        await state.set_state(Authentication.waiting_for_password)
    else:
        await message.answer("✖️ФИО введено не верно")

@dp.message(StateFilter(Authentication.waiting_for_password))
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    parent_name = data.get("parent_name")
    student_name = data.get("student_name")
    password = message.text
    session = Session()
    result = session.query(Parent).filter_by(parent_name=parent_name, student_name=student_name, password=password).first()
    if result:
        await message.answer("Вход успешно выполнен🏆\nВыберите предмет:", reply_markup=kb.subjects)
        await state.set_state(GetGrades.waiting_for_subject)  # <-- Устанавливаем состояние для выбора предмета
    else:
        await message.answer("✖️Данные введены не верно")


@dp.message(StateFilter(GetGrades.waiting_for_subject))
async def get_grades(message: Message, state: FSMContext):
    if message.text.lower() == "выход":
        await message.answer("Выход из просмотра оценок.")
        await state.clear()
        await message.answer("Выберите повторно 👔учитель или 👨‍👩‍👦родитель?", reply_markup=kb.main)
        return
    data = await state.get_data()
    parent_name = data.get("parent_name")
    student_name = data.get("student_name")

    session = Session()
    parent = session.query(Parent).filter_by(parent_name=parent_name, student_name=student_name).first()
    grades = session.query(Grades).filter_by(parent_id=parent.id).first()

    subject = message.text.lower()
    subject_field = {
        'математика': 'math',
        'русский язык': 'russian',
        'литература': 'literature',
        'история': 'history'
    }.get(subject)

    if subject_field and hasattr(grades, subject_field):
        grade = getattr(grades, subject_field)
        await message.answer(f"Оценка по предмету {message.text}: {grade}\nВыберите другой предмет или вернитесь в меню:", reply_markup=kb.subjects)
    else:
        await message.answer("Предмет не найден.\nВыберите предмет или вернитесь в меню:", reply_markup=kb.subjects)

@dp.message(lambda message: message.text == "Выход")
async def exit(message: Message):
    await message.answer("Выберите повторно 👔учитель или 👨‍👩‍👦родитель?", reply_markup=kb.main)
