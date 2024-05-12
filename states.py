from aiogram.fsm.state import StatesGroup, State

class Authentication(StatesGroup):
    waiting_for_parent_name = State()
    waiting_for_student_name = State()
    waiting_for_password = State()

class AddParent(StatesGroup):
    waiting_id = State()
    waiting_for_parent_name = State()
    waiting_for_student_name = State()
    waiting_for_password = State()

class TeacherCode(StatesGroup):
    waiting_code = State()

class AddGrades(StatesGroup):
    waiting_for_parent_id = State()
    waiting_for_math = State()
    waiting_for_russian = State()
    waiting_for_history = State()
    waiting_for_literature = State()

class GetGrades(StatesGroup):
    waiting_for_subject = State()