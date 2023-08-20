from docxtpl import DocxTemplate
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create import bot
import os
from keyboards import napravlenie
import datetime as dt


def get_age(birth):
    today = dt.date.today()
    age = today.year - birth.year
    if today.month < birth.month:
        age -= 1
    elif today.month == birth.month and today.day < birth.day:
        age -= 1
    return age


class FSMAnketa(StatesGroup):
    name_child = State()
    date_birth = State()
    cube_field = State()
    group = State()
    phone_number = State()
    email = State()
    address = State()
    school = State()
    pass_rogd = State()
    snils = State()
    rodstvo1 = State()
    name1 = State()
    job1 = State()
    phone1 = State()
    passport1 = State()
    rodstvo2 = State()
    name2 = State()
    job2 = State()
    phone2 = State()
    passport2 = State()
    end = State()


# @dp.message_handler(lambda c: c.data == 'zayava1', state=None)
async def cm_start(c: types.CallbackQuery):
    await FSMAnketa.name_child.set()
    await bot.send_message(chat_id=c.from_user.id,
                           text='Введите ФИО ребёнка (пример: Фамилия Имя Отчество)'
                                '\nЧтобы выйти из анкеты введите /cancel')
    await bot.answer_callback_query(c.id)


# @dp.message_handler(state="*", commands='cancel')
async def cancel_fsm(m: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await m.answer('Ваше действие было отменено')


# @dp.message_handler(state=FSMAdmin.name_child)
async def set_ch_name(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if (len(m.text.split()) == 2 or len(m.text.split()) == 3) and all(filter(lambda x: x.isalpha(), m.text.split())):
            if len(m.text.split()) == 3:
                data['familiya'], data['imya'], data['otchestvo'] = m.text.split()
            elif len(m.text.split()) == 2:
                data['familiya'], data['imya'] = m.text.split()
                data['otchestvo'] = '-'
            await FSMAnketa.next()
            await m.answer('Введите дату рождения ребёнка (дд.мм.гггг)')
        else:
            await m.answer('Что-то не так. Попробуйте снова')
            await FSMAnketa.name_child.set()


# @dp.message_handler(state=FSMAnketa.date_birth)
async def set_date_birth(m: types.Message, state: FSMContext):
    if all(filter(lambda x: x.isdigit(), m.text.split('.'))):
        async with state.proxy() as data:
            data['date_birthday'] = m.text
        await FSMAnketa.next()
        await m.answer('Выберете направление из предложенных (!редактировать сообщение не нужно!)',
                       reply_markup=napravlenie)
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.date_birth.set()


# @dp.message_handler(state=FSMAnketa.cube_field)
async def set_napravlenie(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if m.text[0] == '@':
            data['napravlenie'] = ' '.join(m.text.split()[1:])
        else:
            data['napravlenie'] = m.text
    await FSMAnketa.next()
    await m.answer('Введите номер группы (число)')


# @dp.message_handler(state=FSMAnketa.group)
async def set_group(m: types.Message, state: FSMContext):
    if m.text.isdigit():
        async with state.proxy() as data:
            data['gruppa'] = m.text
        await FSMAnketa.next()
        await m.answer('Введите номер телефона ребёнка (если его нет, то родителя)\n'
                       'В формате 8ХХХХХХХХХХ')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.group.set()


# @dp.message_handler(state=FSMAnketa.phone_number)
async def set_phone(m: types.Message, state: FSMContext):
    if m.text.isdigit() and len(m.text) == 11 and m.text[0] == '8':
        async with state.proxy() as data:
            data['phone'] = m.text
        await FSMAnketa.next()
        await m.answer('Введите адрес электронной почты')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.phone_number.set()


# @dp.message_handler(state=FSMAnketa.email)
async def set_email(m: types.Message, state: FSMContext):
    if '@' in m.text:
        async with state.proxy() as data:
            data['email'] = m.text
        await FSMAnketa.next()
        await m.answer('Введите адрес поживания ребёнка')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.email.set()


#  @dp.message_handler(state=FSMAnketa.address)
async def set_address(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = m.text
    await FSMAnketa.next()
    await m.answer('Заполните данные о школе в формате тип/номер/название учреждения/класс/буква\n'
                   '(например: школа/4/МБОУ СОШ №4/9/А)')


#  @dp.message_handler(state=FSMAnketa.school)
async def set_school(m: types.Message, state: FSMContext):
    if len(m.text.split('/')) == 5:
        async with state.proxy() as data:
            data['type'], data['number_school'], data['name_school'], data['class'], data['litera'] = m.text.split('/')
        await m.answer('Введите данные паспорта(0000 000000) или свидетельства о рождении ребёнка(V-ЕТ 000000)')
        await FSMAnketa.next()
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.school.set()


# @dp.message_handler(state=FSMAnketa.pass_rogd)
async def set_passport(m: types.Message, state: FSMContext):
    if len(m.text.split()) == 2 and (len(m.text.split()[0]) == 4 and m.text.split()[0].isdigit() or '-' in m.text.split()[0])\
            and (len(m.text.split()[1]) == 6 and m.text.split()[1].isdigit()):
        async with state.proxy() as data:
            data['series'], data['nomer'] = m.text.split()
        await FSMAnketa.next()
        await m.answer('Введите данные СНИЛС ребёнка (000-000-000 00)')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.pass_rogd.set()


#  @dp.message_handler(state=FSMAnketa.snils)
async def set_snils(m: types.Message, state: FSMContext):
    s = m.text.split()
    if len(s) == 2 and len(s[0].split('-')) == 3 and all(filter(lambda x: len(x) == 3, s[0].split('-'))):
        async with state.proxy() as data:
            data['snils'] = m.text
        await m.answer('Заполните анкету первого родителя:')
        await FSMAnketa.next()
        await m.answer('Вид родства (мать, отец или др.)')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.snils.set()


# @dp.message_handler(state=FSMAnketa.rodstvo1)
async def set_rodstvo1(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rodstvo1'] = m.text
    await FSMAnketa.next()
    await m.answer('ФИО первого родителя (Фамилия Имя Отчество)')


# @dp.message_handler(state=FSMAnketa.name1)
async def set_name1(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(m.text.split()) == 2 or len(m.text.split()) == 3:
            if len(m.text.split()) == 3:
                data['familiya1'], data['imya1'], data['otchestvo1'] = m.text.split()
            elif len(m.text.split()) == 2:
                data['familiya1'], data['imya1'] = m.text.split()
                data['otchestvo1'] = '-'
            await FSMAnketa.next()
            await m.answer('Работа родителя (место работы/должность)')
        else:
            await m.answer('Что-то не так. Попробуйте снова')
            await FSMAnketa.name1.set()


# @dp.message_handler(state=FSMAnketa.job1)
async def set_job1(m: types.Message, state: FSMContext):
    if '/' in m.text and m.text.count('/') == 1:
        async with state.proxy() as data:
            data['place_job1'], data['job1'] = m.text.split('/')
        await FSMAnketa.next()
        await m.answer('Номер телефона первого родителя\nВ формате 8ХХХХХХХХХХ')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.job1.set()


# @dp.message_handler(state=FSMAnketa.phone1)
async def set_phone1(m: types.Message, state: FSMContext):
    if m.text.isdigit() and len(m.text) == 11 and m.text[0] == '8':
        async with state.proxy() as data:
            data['phone1'] = m.text
        await FSMAnketa.next()
        await m.answer('Серия и номер паспорта первого родителя через пробел (0000 000000)')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.phone1.set()


# @dp.message_handler(state=FSMAnketa.passport1)
async def set_passport1(m: types.Message, state: FSMContext):
    if len(m.text.split()) and len(m.text.split()[0]) == 4 and len(m.text.split()[1]) == 6:
        async with state.proxy() as data:
            data['series1'], data['nomer1'] = m.text.split()
        await FSMAnketa.next()
        await m.answer('Введите вид родства второго родителя или напишите "Нет"')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.passport1.set()


# @dp.message_handler(state=FSMAnketa.rodstvo2)
async def set_rodstvo2(m: types.Message, state: FSMContext):
    if m.text.lower().strip() != 'нет':
        async with state.proxy() as data:
            data['rodstvo2'] = m.text
        await FSMAnketa.next()
        await m.answer('ФИО второго родителя (Фамилия Имя Отчество)')
    else:
        await FSMAnketa.end.set()
        await m.answer('Проверьте свои ответы и, если вы хотите продолжить, введите "да"'
                       '(!будьте внимательны, ведь в случае ошибки все ответы будут сброшены!)')


# @dp.message_handler(state=FSMAnketa.name2)
async def set_name2(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(m.text.split()) == 2 or len(m.text.split()) == 3:
            if len(m.text.split()) == 3:
                data['familiya2'], data['imya2'], data['otchestvo2'] = m.text.split()
            elif len(m.text.split()) == 2:
                data['familiya2'], data['imya2'] = m.text.split()
                data['otchestvo2'] = '-'
            await FSMAnketa.next()
            await m.answer('Работа родителя (место работы/должность)')
        else:
            await m.answer('Что-то не так. Попробуйте снова')
            await FSMAnketa.name2.set()


# @dp.message_handler(state=FSMAnketa.job2)
async def set_job2(m: types.Message, state: FSMContext):
    if '/' in m.text and m.text.count('/') == 1:
        async with state.proxy() as data:
            data['place_job2'], data['job2'] = m.text.split('/')
        await FSMAnketa.next()
        await m.answer('Номер телефона второго родителя')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.job2.set()


# @dp.message_handler(state=FSMAnketa.phone2)
async def set_phone2(m: types.Message, state: FSMContext):
    if m.text.isdigit() and len(m.text) == 11 and m.text[0] == '8':
        async with state.proxy() as data:
            data['phone2'] = m.text
        await FSMAnketa.next()
        await m.answer('Серия и номер паспорта второго родителя через пробел (0000 000000)')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.phone2.set()


# @dp.message_handler(state=FSMAnketa.passoport2)
async def set_passport2(m: types.Message, state: FSMContext):
    if len(m.text.split()) and len(m.text.split()[0]) == 4 and len(m.text.split()[1]) == 6:
        async with state.proxy() as data:
            data['series2'], data['nomer2'] = m.text.split()
        await FSMAnketa.next()
        await m.answer('Если вы хотите продолжить, введите "да"'
                       '(!будьте внимательны, ведь в случае ошибки все ответы будут сброшены!)')
    else:
        await m.answer('Что-то не так. Попробуйте снова')
        await FSMAnketa.passport2.set()


# @dp.message_handler(state=FSMAnketa.end)
async def end(m: types.Message, state: FSMContext):
    if m.text.lower().strip() == 'да':
        async with state.proxy() as data:
            date = dt.date(m.date.year, m.date.month, m.date.day)
            data['date'] = date.strftime('%d.%m.%Y')
            doc = DocxTemplate("documents/templates/zayava_1.docx")
            doc.render(data)
            doc.save('documents/zayava' + f'{m.from_user.id}' + '.docx')
            doc1 = DocxTemplate('documents/templates/soglasie.docx')
            doc1.render(data)
            doc1.save('documents/soglasie' + f'{m.from_user.id}' + '.docx')
            d, month, y = list(map(int, data['date_birthday'].split('.')))
            age = get_age(dt.date(y, month, d))
        await m.answer_document(open('documents/zayava' + f'{m.from_user.id}' + '.docx', 'rb'))
        os.remove('documents/zayava' + f'{m.from_user.id}' + '.docx')
        await m.answer_document(open('documents/soglasie' + f'{m.from_user.id}' + '.docx', 'rb'))
        os.remove('documents/soglasie' + f'{m.from_user.id}' + '.docx')
        if age < 12:
            await m.answer('Так как вашему ребёнку нет 12 лет, также заполните следующий документ ВРУЧНУЮ:')
            await m.answer_document(document=open('documents/templates/nottwelve.docx', 'rb'))
            os.remove('documents/templates/nottwelve.docx')
        await state.finish()
        await m.answer('Готово!')
    else:
        await state.finish()
        await FSMAnketa.name_child.set()


def register_handlers_zayava(dp: Dispatcher):
    dp.register_callback_query_handler(cm_start, lambda c: c.data == 'zayava1', state=None)
    dp.register_message_handler(cancel_fsm, state="*", commands='cancel')
    dp.register_message_handler(set_ch_name, state=FSMAnketa.name_child)
    dp.register_message_handler(set_date_birth, state=FSMAnketa.date_birth)
    dp.register_message_handler(set_napravlenie, state=FSMAnketa.cube_field)
    dp.register_message_handler(set_group, state=FSMAnketa.group)
    dp.register_message_handler(set_phone, state=FSMAnketa.phone_number)
    dp.register_message_handler(set_email, state=FSMAnketa.email)
    dp.register_message_handler(set_address, state=FSMAnketa.address)
    dp.register_message_handler(set_school, state=FSMAnketa.school)
    dp.register_message_handler(set_passport, state=FSMAnketa.pass_rogd)
    dp.register_message_handler(set_snils, state=FSMAnketa.snils)
    dp.register_message_handler(set_rodstvo1, state=FSMAnketa.rodstvo1)
    dp.register_message_handler(set_name1, state=FSMAnketa.name1)
    dp.register_message_handler(set_job1, state=FSMAnketa.job1)
    dp.register_message_handler(set_phone1, state=FSMAnketa.phone1)
    dp.register_message_handler(set_passport1, state=FSMAnketa.passport1)
    dp.register_message_handler(set_rodstvo2, state=FSMAnketa.rodstvo2)
    dp.register_message_handler(set_name2, state=FSMAnketa.name2)
    dp.register_message_handler(set_job2, state=FSMAnketa.job2)
    dp.register_message_handler(set_phone2, state=FSMAnketa.phone2)
    dp.register_message_handler(set_passport2, state=FSMAnketa.passport2)
    dp.register_message_handler(end, state=FSMAnketa.end)
